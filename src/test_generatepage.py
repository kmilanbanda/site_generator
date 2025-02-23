import unittest
from generatepage import extract_title


class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self):
        test = "# Title"
        title = extract_title(test)
        self.assertEqual(title, test[2:])

    def test_extract_title_full_md(self):
        md = """
# This is the Title

> this is some
> other stuff
"""
        title = extract_title(md)
        test = "This is the Title"
        self.assertEqual(title, test)

    def test_invalid_header(self):
        md = """
## This is the Title
"""
        with self.assertRaises(Exception):
            title = extract_title(md)

    def test_random_order_headers(self):
        md = """
### Header 3

# Title

## Header 2
"""
        self.assertEqual(extract_title(md), "Title")

    def test_multiple_headers(self):
        md = """
# Title

# Not The Title
"""
        self.assertEqual(extract_title(md), "Title")
if __name__ == "__main__":
    unittest.main()
