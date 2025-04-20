import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("p", "Sample text", None, {"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')
    
    def test_repr(self):
        node = HTMLNode("*", "repr sample text!")
        self.assertEqual(isinstance(node.__repr__(), str), True)
        
    def test_empty_case(self):
        node = HTMLNode
        node2 = HTMLNode
        self.assertEqual(node, node2)

    """def test_to_html(self):
        node = HTMLNode("p", "Sample text", None, {"href": "https://www.google.com"})
        try:
            node.to_html()
        except NotImplementedError:
            self.assertEqual(True, True)
        except:
            self.assertEqual(True, False) """

if __name__ == "__main__":
    unittest.main()
