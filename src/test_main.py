import unittest
from main import (
    extract_titel
)

class TestFunctions(unittest.TestCase):
    def test_extract_titel(self):
        heading = extract_titel("# This is a heading")
        self.assertEqual(heading, "This is a heading")
        with self.assertRaises(Exception):
            heading = extract_titel("## This is not a h1 heading")

        
