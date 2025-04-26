from textnode import *
from leafnode import *
from parentnode import *
from otherfunctions import *
from blocks import *

def main():
    test_node = LeafNode("*", "Bold text Leaf Node")
    #print(test_node)
    test_parent = ParentNode("b", test_node)
    #print(test_parent.to_html())
    md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
"""
    print(block_to_block_type(""))
    return



    




if __name__ == "__main__":
    main()