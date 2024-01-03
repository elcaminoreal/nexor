import argparse
import functools
import logging
from typing import Sequence, Mapping, Callable
import subprocess
import sys

import gather
from gather.commands import add_argument

LOGGER = logging.getLogger(__name__)

_SUBCOMMANDS = gather.Collector()

def command(*args, name=None):
    return _SUBCOMMANDS.register(
        transform=gather.Wrapper.glue(args),
        name=name,
    )


@command(
    add_argument("--no-dry-run", action="store_true", default=False),
    add_argument("-d", "--description", required=True),
)
def init(args):  # pragma: no cover
    # Eventually,
    # use `git` to get the details:
    #
    # --data VARIABLE=VALUE
    # `project_name`/`organization`:
    # parse `git remote get-url origin`
    # parse `git log --max-count 1 --format=email`
    # for `maintainer_name`, `maintainer_email`
    # `short_description` from args.
    args.run(
        [
            sys.executable,
            "-m",
            "copier",
            "copy",
            "gh:moshez/python-standard.git",
            args.env["PWD"],
        ],
        capture_output=False,
    )

def wrap_run(args):  # pragma: no cover
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

def main(
    *, argv: Sequence[str], env: Mapping[str, str], run: Callable
) -> None:  # pragma: no cover
    def error(args):
        parser.print_help()
        raise SystemExit(1)

    commands = gather.unique(_SUBCOMMANDS.collect())
    parser = argparse.ArgumentParser()
    parser.set_defaults(
        command=error,
        env=env,
        orig_run=run,
    )
    subparsers = parser.add_subparsers()
    for name, value in commands.items():
        func, args = value.original, value.extra
        a_subparser = subparsers.add_parser(name)
        a_subparser.set_defaults(command=func)
        for argset in args:
            a_subparser.add_argument(*argset.args, **dict(argset.kwargs))
    args = parser.parse_args(argv[1:])
    wrap_run(args)
    args.command(args)
