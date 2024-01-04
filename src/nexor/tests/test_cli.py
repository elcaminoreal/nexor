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

class TestWrap(unittest.TestCase): # pragma: no cover
    def test_dry_run(self):
        with contextlib.ExitStack() as stack:
            tmp_dir = pathlib.Path(stack.enter_context(tempfile.TemporaryDirectory()))
            cli.main(
                run=subprocess.run,
                argv=["nexor", "self_test", "--output-dir", os.fspath(tmp_dir)],
                env={},
            )
            contents = {
                child.name: child.read_text()
                for child in tmp_dir.iterdir()
            }
        assert_that(
            contents,
            all_of(
                not_(has_key("unsafe.txt")),
                has_entry("safe.txt", "2"),
           ),
        )

    def test_no_dry_run(self):
        with contextlib.ExitStack() as stack:
            tmp_dir = pathlib.Path(stack.enter_context(tempfile.TemporaryDirectory()))
            cli.main(
                run=subprocess.run,
                argv=["nexor", "self_test", "--output-dir", os.fspath(tmp_dir), "--no-dry-run"],
                env={},
            )
            contents = {
                child.name: child.read_text()
                for child in tmp_dir.iterdir()
            }
        assert_that(
            contents,
            all_of(
                has_entry("unsafe.txt", "2"),
                has_entry("safe.txt", "2"),
           ),
        )

    def test_fail(self):
        with contextlib.ExitStack() as stack:
            tmp_dir = pathlib.Path(stack.enter_context(tempfile.TemporaryDirectory()))
            assert_that(calling(cli.main).with_args(
                run=subprocess.run,
                argv=["nexor", "self_test", "--output-dir", os.fspath(tmp_dir / "not-there")],
                env={},
            ),
                raises(subprocess.CalledProcessError),
                       )