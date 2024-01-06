from gather import entry

from . import cli

entry.dunder_main(
    globals_dct=globals(),
    command_data=cli.ENTRY_DATA,
)
