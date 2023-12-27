import unittest
from hamcrest import assert_that, contains_string

from .. import __version__
from .. import cli
from .. import lock


class TestInit(unittest.TestCase):
    def test_version(self):
        assert_that(__version__, contains_string("."))
