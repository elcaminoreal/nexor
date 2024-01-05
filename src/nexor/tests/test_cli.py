import contextlib
import unittest
from hamcrest import (
    assert_that,
    calling,
    contains_string,
    raises,
)
from unittest import mock
from io import StringIO

from .. import cli


class TestMain(unittest.TestCase):  # pragma: no cover
    def test_help(self):
        with contextlib.ExitStack() as stack:
            stdout = stack.enter_context(mock.patch("sys.stdout", new=StringIO()))
            assert_that(
                calling(cli.main).with_args(
                    run=lambda: None,
                    argv=["nexor"],
                    env={},
                ),
                raises(SystemExit),
            )
        assert_that(stdout.getvalue(), contains_string("usage:"))
