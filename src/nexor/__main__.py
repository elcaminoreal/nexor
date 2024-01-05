import os
import logging
import subprocess
import sys

from gather import commands as commandslib

from . import cli

if __name__ != "__main__":
    raise ImportError("module cannot be imported", __name__)

logging.basicConfig(
    format="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
    level=logging.INFO,
)

commandslib.run_maybe_dry(
    parser=commandslib.set_parser(collected=cli.SUBCOMMANDS.collect()),
    is_subcommand=globals().get("IS_SUBCOMMAND", False),
    prefix="nexor",
)
