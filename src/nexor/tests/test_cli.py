import contextlib
import unittest
import logging
from hamcrest import (
    assert_that,
    contains_string,
)
from unittest import mock
from io import StringIO

from gather import entry

from .. import cli


class TestMain(unittest.TestCase):  # pragma: no cover
    def test_version(self):
        with contextlib.ExitStack() as stack:
            stdout = stack.enter_context(mock.patch("sys.stdout", new=StringIO()))
            argv = stack.enter_context(mock.patch("sys.argv", new=[]))
            argv[:] = ["nexor", "version"]
            entry.dunder_main(
                globals_dct=dict(__name__="__main__"),
                command_data=cli.ENTRY_DATA,
                logger=logging.Logger("nonce"),
            )
        assert_that(stdout.getvalue(), contains_string("20"))
