import datetime
import unittest

from argparse import ArgumentTypeError

from cmdline import util


class UtilTestCase(unittest.TestCase):
    def test_listify(self):
        expected = ['a', 'b']
        self.assertEqual(expected, util.listify('a,b'))

    def test_listify_with_spaces(self):
        expected = ['a', 'b']
        self.assertEqual(expected, util.listify(' a,   b  '))

    def test_date(self):
        expected = datetime.datetime(2014, 9, 26).date()

        self.assertEqual(expected, util.date('2014-09-26'))

    def test_bad_date(self):
        self.assertRaises(ArgumentTypeError, util.date, '2014/09/26')

