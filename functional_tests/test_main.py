import unittest
import sys
import os
from StringIO import StringIO

from leadsheets.core import main

CURRENT_DIR = os.path.dirname(__file__)


class TestMain(unittest.TestCase):
    def setUp(self):
        self.saved_stdout = sys.stdout
        sys.stdout = StringIO()

    def tearDown(self):
        sys.stdout = self.saved_stdout

    def test_main(self):
        sys.argv.insert(1, os.path.join(CURRENT_DIR, 'example.csv'))
        main()
        self.assertEqual(sys.stdout.getvalue(), '''3, bronze, 0
1, bronze, 7
2, platinum, 100
''')
