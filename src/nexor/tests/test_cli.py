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
                    is_subcommand=False,
                ),
                raises(SystemExit),
            )
        assert_that(stdout.getvalue(), contains_string("usage:"))

    def test_version(self):
        with contextlib.ExitStack() as stack:
            stdout = stack.enter_context(mock.patch("sys.stdout", new=StringIO()))
            cli.main(
                run=lambda: None,
                argv=["nexor-version"],
                env={},
                is_subcommand=True,
            )
        assert_that(stdout.getvalue(), contains_string("20"))
