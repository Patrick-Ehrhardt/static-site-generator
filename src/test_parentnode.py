import unittest

from parentnode import *
from leafnode import *


class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_multiple_children(self):
        child_node = LeafNode("b", "Bold text")
        child_node2 = LeafNode("i", "Italic text")
        parent_node = ParentNode("span", [child_node, child_node2])
        grandparent_node = ParentNode("div", parent_node)
        self.assertEqual(
            grandparent_node.to_html(), 
            "<div><span><b>Bold text</b><i>Italic text</i></span></div>"
        )
    
    def test_mixed_nested_nodes(self):
        child_node = LeafNode("b", "Bold text")
        child_node2 = LeafNode("i", "Italic text")
        parent_node = ParentNode("span", child_node)
        parent_node2 = ParentNode("div", [parent_node, child_node2])
        parent_node3 = ParentNode("tag", parent_node2)
        self.assertEqual(parent_node3.to_html(), "<tag><div><span><b>Bold text</b></span><i>Italic text</i></div></tag>")

    def test_missing_child(self):
        child_node = LeafNode("b", "Bold text")
        parent_node = ParentNode("div", [child_node, None])
        self.assertEqual(parent_node.to_html(), "<div><b>Bold text</b></div>")

    

if __name__ == "__main__":
    unittest.main()
