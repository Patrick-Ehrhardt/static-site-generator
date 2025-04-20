from textnode import *
from leafnode import *
from parentnode import *

def main():
    test_node = LeafNode("*", "Bold text Leaf Node")
    print(test_node)
    test_parent = ParentNode("b", test_node)
    print(test_parent.to_html())
    node = ParentNode(
    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ],
)

    print(node.to_html())

    return



    




if __name__ == "__main__":
    main()