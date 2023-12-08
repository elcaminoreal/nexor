import os
import subprocess
import sys

from . import cli

if __name__ != "__main__":
    raise ImportError("module cannot be imported")

cli.main(
    argv=sys.argv,
    env=os.environ,
    run=subprocess.run,
)
   