import argparse
import functools
from typing import Sequence, Mapping, Callable
import sys

import gather
from gather.commands import add_argument

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
    make_execute(args)(
        [
            sys.executable,
            "-m",
            "copier",
            "copy",
            "gh:moshez/python-standard.git",
            ".",
        ]
    )


def make_execute(args):  # pragma: no cover
    def _wrapped(command, **kwargs):
        print("Command", *command)
        if args.no_dry_run:
            return args.run(command, **kwargs)
        else:
            print("Dry run, skipping")

    return _wrapped


def wrap_run(run):  # pragma: no cover
    # Eventually add notes
    return functools.partial(
        run,
        # capture_output=True,
        text=True,
        check=True,
    )


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
        run=wrap_run(run),
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
    args.command(args)
