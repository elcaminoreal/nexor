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
from gather.commands import add_argument
from gather import commands as commandslib

LOGGER = logging.getLogger(__name__)

_SUBCOMMANDS = gather.Collector()

command = commandslib.make_command_register(_SUBCOMMANDS)
    
def main(
    *, argv: Sequence[str], env: Mapping[str, str], run: Callable
) -> None:
    def error(args):
        parser.print_help()
        raise SystemExit(1)
    parser = argparse.ArgumentParser()
    parser.set_defaults(__gather_command__=error)
    commandslib.run_maybe_dry(   
        parser=commandslib.set_parser(parser=parser, collected=_SUBCOMMANDS.collect()),
        argv=argv,
        env=env,
        sp_run=run,
    )
