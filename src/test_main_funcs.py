import unittest
from main import extract_title

class TestMainFunctions(unittest.TestCase):
    def test_extract_title(self):
        self.assertEqual(
            extract_title("# Hello"),
            "Hello"
        )

    def test_extract_title_no_title(self):
        with self.assertRaises(Exception):
            extract_title("Hello")