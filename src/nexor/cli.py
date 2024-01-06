import argparse
import functools
import logging
from typing import Sequence, Mapping, Callable
import runpy

from gather import entry

from . import __version__
    
ENTRY_DATA = entry.EntryData.create("nexor")
command = ENTRY_DATA.register

@command()
def version(args: argparse.ArgumentParser) -> None:
    print(__version__)
