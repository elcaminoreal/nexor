import contextlib
import unittest
from hamcrest import assert_that, all_of, not_, calling, contains_string, has_entry, has_key, raises
from unittest import mock
import pathlib
import os
import tempfile
import subprocess
from io import StringIO

from .. import cli

class TestMain(unittest.TestCase): # pragma: no cover
    def test_help(self):
        with contextlib.ExitStack() as stack:
            stdout = stack.enter_context(mock.patch("sys.stdout", new=StringIO()))
            stderr = stack.enter_context(mock.patch("sys.stderr", new=StringIO()))
            assert_that(
                calling(cli.main).with_args(
                    run=lambda:None,
                    argv=["nexor"],
                    env={},
                ),
                raises(SystemExit),
            )
        assert_that(stdout.getvalue(), contains_string("usage:"))
