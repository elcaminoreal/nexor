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
    commandslib.run_maybe_dry(   
        parser=commandslib.set_parser(collected=_SUBCOMMANDS.collect()),
        argv=argv,
        env=env,
        sp_run=run,
    )
