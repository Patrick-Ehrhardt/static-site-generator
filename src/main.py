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
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

    md = """
1. Get groceries
2. Write code
3. Go to bed
"""
    node = markdown_to_html_node(md)
    html = node.to_html()
    print(html)
    return



    




if __name__ == "__main__":
    main()