import argparse
import functools
import logging
from typing import Sequence, Mapping, Callable
import runpy

import gather
from gather import commands as commandslib
import toolz

from . import __version__

LOGGER = logging.getLogger(__name__)
SUBCOMMANDS = gather.Collector()
command = commandslib.make_command_register(SUBCOMMANDS)


@command()
def version(args):
    print(__version__)
    raise SystemExit(0)

main_command = toolz.compose(
    lambda _ignored: None,
    functools.partial(
        runpy.run_module,
        "nexor",
        run_name="__main__",
    ),
)

sub_command = toolz.compose(
    lambda _ignored: None,
    functools.partial(
        runpy.run_module,
        "nexor",
        run_name="__main__",
        init_globals=dict(IS_SUBCOMMAND=True),
    ),
)
