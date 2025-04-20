import unittest

from leafnode import *


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_link(self):
        node = LeafNode("a", "Click Here!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click Here!</a>')

    def test_leaf_no_tag(self):
        node = LeafNode(None, "Plain text please")
        self.assertEqual(node.to_html(), "Plain text please")

if __name__ == "__main__":
    unittest.main()
