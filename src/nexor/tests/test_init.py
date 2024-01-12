import unittest
from hamcrest import assert_that, contains_string

from .. import __version__, ENTRY_DATA


class TestInit(unittest.TestCase):
    def test_version(self):
        assert_that(__version__, contains_string("."))

    def test_collect(self):
        ENTRY_DATA.collector.collect()
