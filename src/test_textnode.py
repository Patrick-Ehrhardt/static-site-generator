import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_repr(self):
        node = TextNode("Sample node", TextType.ITALIC, "127.0.0.1:32400")
        self.assertEqual(isinstance(node.__repr__(), str), True)
        

if __name__ == "__main__":
    unittest.main()
