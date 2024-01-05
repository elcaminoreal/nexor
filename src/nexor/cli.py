import argparse
import functools
import logging
from typing import Sequence, Mapping, Callable
import runpy

import gather.commands
import toolz

from . import __version__

SUBCOMMANDS = gather.Collector()
command = gather.commands.make_command_register(SUBCOMMANDS)


@command()
def version(args: argparse.ArgumentParser) -> None:
    print(__version__)
    
ns = argparse.Namespace()

    
main_command = toolz.compose(
    lambda _ignored: None,
    functools.partial(
        runpy.run_module,
        "nexor",
        run_name="__main__",
    ),
)

ns.sub_command = functools.partial(main_command, init_globals=dict(IS_SUBCOMMAND=True))
