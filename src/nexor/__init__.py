import importlib.metadata
from gather import entry

ENTRY_DATA = entry.EntryData.create("nexor")

__version__ = importlib.metadata.version(__name__)
