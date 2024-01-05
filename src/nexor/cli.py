import argparse
import functools
import logging
import os
import pathlib
import textwrap
from typing import Sequence, Mapping, Callable
import subprocess
import sys

import gather
from gather.commands import add_argument, make_command_register

LOGGER = logging.getLogger(__name__)

_SUBCOMMANDS = gather.Collector()


#def command(*args, name=None):
#    return _SUBCOMMANDS.register(
#        transform=gather.Wrapper.glue(args),
#        name=name,
#    )

command = make_command_register(_SUBCOMMANDS)

def _wrap_run(args):
    orig_run = args.orig_run

    @functools.wraps(orig_run)
    def wrapped_run(cmdargs, **kwargs):
        real_kwargs = dict(text=True, check=True, capture_output=True)
        real_kwargs.update(kwargs)
        LOGGER.info("Running: %s", cmdargs)
        try:
            return orig_run(cmdargs, **real_kwargs)
        except subprocess.CalledProcessError as exc:
            exc.add_note(f"STDERR: {exc.stderr}")
            exc.add_note(f"STDOUT: {exc.stdout}")
            raise

    @functools.wraps(orig_run)
    def wrapped_dry_run(cmdargs, **kwargs):
        LOGGER.info("Running: %s", cmdargs)
        LOGGER.info("Dry run, skipping")

    unsafe_run = wrapped_run if args.no_dry_run else wrapped_dry_run
    args.run = unsafe_run
    args.safe_run = wrapped_run

@command(
    add_argument("--no-dry-run", action="store_true", default=False),
    add_argument("--output-dir", required=True),
)
def self_test(args):
    output_dir = pathlib.Path(args.output_dir)
    safe = os.fspath(output_dir / "safe.txt")
    unsafe = os.fspath(output_dir / "unsafe.txt")
    code = textwrap.dedent("""\
    import pathlib
    import sys
    pathlib.Path(sys.argv[1]).write_text(str(1 + 1))
    """)
    args.run([sys.executable, "-c", code, unsafe])
    args.safe_run([sys.executable, "-c", code, safe])
    
def main(
    *, argv: Sequence[str], env: Mapping[str, str], run: Callable
) -> None:
    def error(args):
        parser.print_help()
        raise SystemExit(1)

    commands = gather.unique(_SUBCOMMANDS.collect())
    parser = argparse.ArgumentParser()
    parser.set_defaults(
        command=error,
        env=env,
        orig_run=run,
        no_dry_run=False,
    )
    subparsers = parser.add_subparsers()
    for name, value in commands.items():
        func, args = value.original, value.extra
        a_subparser = subparsers.add_parser(name)
        a_subparser.set_defaults(command=func)
        for argset in args:
            a_subparser.add_argument(*argset.args, **dict(argset.kwargs))
    args = parser.parse_args(argv[1:])
    _wrap_run(args)
    args.command(args)
