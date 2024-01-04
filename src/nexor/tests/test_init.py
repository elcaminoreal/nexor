import unittest
from hamcrest import assert_that, contains_string

from .. import __version__
from .. import cli
from .. import lock


class TestInit(unittest.TestCase):
    def test_version(self):
        assert_that(__version__, contains_string("."))

    def test_cli(self):
        assert_that(cli.__doc__ or "", contains_string(""))

    def test_lock(self):
        assert_that(lock.__doc__ or "", contains_string(""))
