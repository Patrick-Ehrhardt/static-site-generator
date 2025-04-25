from textnode import *
from leafnode import *
from parentnode import *
from otherfunctions import *

def main():
    test_node = LeafNode("*", "Bold text Leaf Node")
    #print(test_node)
    test_parent = ParentNode("b", test_node)
    #print(test_parent.to_html())
    node = TextNode("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)", TextType.TEXT)
    new_nodes = text_to_textnodes("![image one](https://imgur.com) and some **bold** text")
    for node in new_nodes:
        print(node)
    text = "**leading split**"
    print(text.split("**"))
    return



    




if __name__ == "__main__":
    main()