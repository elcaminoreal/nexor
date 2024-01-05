import os
import logging
import subprocess
import sys

from . import cli

if __name__ != "__main__":
    raise ImportError("module cannot be imported", __name__)

logging.basicConfig(
    format="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
    level=logging.INFO,
)
cli.main(
    argv=sys.argv,
    env=os.environ,
    run=subprocess.run,
    is_subcommand=globals().get("IS_SUBCOMMAND", False),
)
