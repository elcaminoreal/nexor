import argparse
import logging
from typing import Sequence, Mapping, Callable
import runpy

import gather
from gather import commands as commandslib

from . import __version__

LOGGER = logging.getLogger(__name__)

_SUBCOMMANDS = gather.Collector()

command = commandslib.make_command_register(_SUBCOMMANDS)

@command()
def version(args):
    print(__version__)

def main(*, argv: Sequence[str], env: Mapping[str, str], run: Callable, is_subcommand: bool) -> None:
    def error(args):
        parser.print_help()
        raise SystemExit(1)

    parser = argparse.ArgumentParser()
    parser.set_defaults(__gather_command__=error)

    argv = list(argv)
    if is_subcommand:
        argv[0:0] = ["nexor"]
        argv[1] = argv[1].rsplit("/", 1)[-1]
        argv[1] = argv[1].removeprefix("nexor-")

    commandslib.run_maybe_dry(
        parser=commandslib.set_parser(parser=parser, collected=_SUBCOMMANDS.collect()),
        argv=argv,
        env=env,
        sp_run=run,
    )

def main_command(): # pragma: no cover
    runpy.run_module("nexor", run_name="__main__")

def sub_command(): # pragma: no cover
    runpy.run_module("nexor", run_name="__main__", init_globals=dict(IS_SUBCOMMAND=True))