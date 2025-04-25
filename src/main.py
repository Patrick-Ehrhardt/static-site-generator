from textnode import *
from leafnode import *
from parentnode import *
from otherfunctions import *

def main():
    test_node = LeafNode("*", "Bold text Leaf Node")
    #print(test_node)
    test_parent = ParentNode("b", test_node)
    #print(test_parent.to_html())
    node = ParentNode(
    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ],
)

   # print(node.to_html())

    node = TextNode("I _dont_ want _to_ write _this_ test", TextType.TEXT)
    new_node = split_nodes_delimiter(node, "_", TextType.ITALIC)
    #print(new_node)

    matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and then another image link ![image](imgur.com/alt)")
    #print(matches)
    matches = extract_markdown_links("This text includes a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
    #print(matches)

    
    new_nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
    for node in new_nodes:
        print(node)
    return



    




if __name__ == "__main__":
    main()