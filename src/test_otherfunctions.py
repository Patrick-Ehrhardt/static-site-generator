import unittest

from otherfunctions import *
from textnode import *



class TestOtherFunctions(unittest.TestCase):

    #Tests for split node image and links

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_image(self):
        node = TextNode("This node has one ![image](https://imagewebsite.com)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual( new_nodes, 
            [
                TextNode("This node has one ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://imagewebsite.com")
            ]
        )

    def test_image_first(self):
        node = TextNode("![image](https://notimagewebsite.com) at the beginning", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual( new_nodes, 
                             [
                                 TextNode("image", TextType.IMAGE, "https://notimagewebsite.com"),
                                 TextNode(" at the beginning", TextType.TEXT)
                             ])
    
    def test_two_images_first(self):
        node = TextNode("![first](https://website.com)![second](https://notwebsite.com) bottom text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual( new_nodes, 
                             [
                                 TextNode("first", TextType.IMAGE, "https://website.com"),
                                 TextNode("second", TextType.IMAGE, "https://notwebsite.com"),
                                 TextNode(" bottom text", TextType.TEXT)
                             ])
        
    def test_image_first_last(self):
        node = TextNode("![first](https://website.com) and middle text before ![last](https://notwebsite.com)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual( new_nodes,
                             [
                                 TextNode("first", TextType.IMAGE, "https://website.com"),
                                 TextNode(" and middle text before ", TextType.TEXT),
                                 TextNode("last", TextType.IMAGE, "https://notwebsite.com")
                             ])
        
    def test_image_empty(self):
        node = TextNode("This node has no image", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [TextNode("This node has no image", TextType.TEXT)])

    def test_split_links(self):
        node = TextNode("This node has a [link](https://toawebsite.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes,
                             [
                                 TextNode("This node has a ", TextType.TEXT),
                                 TextNode("link", TextType.LINK, "https://toawebsite.com")
                             ])
        
    def test_split_two_links(self):
        node = TextNode("This node has [link](boot.dev) and [second link](notboot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes,
                             [
                                 TextNode("This node has ", TextType.TEXT),
                                 TextNode("link", TextType.LINK, "boot.dev"),
                                 TextNode(" and ", TextType.TEXT),
                                 TextNode("second link", TextType.LINK, "notboot.dev")
                             ])
        
    def test_leading_link(self):
        node = TextNode("[link](boot.dev) leading link", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes,
                             [
                                 TextNode("link", TextType.LINK, "boot.dev"),
                                 TextNode(" leading link", TextType.TEXT)
                             ])
        
    def test_empty_link(self):
        node = TextNode("This node has no link", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [TextNode("This node has no link", TextType.TEXT)])

    def test_blank_link(self):
        node = TextNode("This has an empty link []()", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [TextNode("This has an empty link ", TextType.TEXT)])

    def test_split_mixed_list(self):
        node = [
            TextNode("This text is the ", TextType.TEXT),
            TextNode("beginning", TextType.BOLD),
            TextNode(" of the node with a [link](https://website.com)", TextType.TEXT)
        ]
        new_nodes = split_nodes_link(node)
        print(f"new_nodes: {new_nodes}")
        self.assertListEqual(new_nodes,
                             [
                                TextNode("This text is the ", TextType.TEXT),
                                TextNode("beginning", TextType.BOLD),
                                TextNode(" of the node with a ", TextType.TEXT),
                                TextNode("link", TextType.LINK, "https://website.com")
                             ])
        
    def test_split_mixed_image(self):
        node = [
            TextNode("This text has ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode("text. Plus an ![image](https://imgur.com)", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(node)
        self.assertListEqual( new_nodes, 
                             [
                            TextNode("This text has ", TextType.TEXT),
                            TextNode("bold", TextType.BOLD),
                            TextNode(" and ", TextType.TEXT),
                            TextNode("italic", TextType.ITALIC),
                            TextNode("text. Plus an ", TextType.TEXT),
                            TextNode("image", TextType.IMAGE, "https://imgur.com")
                             ])
        
    def test_centered_image(self):
        node = [
            TextNode("This text has a ![leading image](https://differentpicture.com)", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode("text. Plus an ![image](https://imgur.com)", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(node)
        self.assertListEqual( new_nodes, 
                             [
                            TextNode("This text has a ", TextType.TEXT),
                            TextNode("leading image", TextType.IMAGE, "https://differentpicture.com"),
                            TextNode("bold", TextType.BOLD),
                            TextNode(" and ", TextType.TEXT),
                            TextNode("italic", TextType.ITALIC),
                            TextNode("text. Plus an ", TextType.TEXT),
                            TextNode("image", TextType.IMAGE, "https://imgur.com")
                             ])
        
    def test_leading_image(self):
        node = [
            TextNode("![leading image](https://imgur.com) and some following text", TextType.TEXT),
            TextNode(" plus some bold", TextType.BOLD),
            TextNode("and another ![image](https://imgur.com) to follow", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(node)
        self.assertListEqual( new_nodes, 
                             [
                                 TextNode("leading image", TextType.IMAGE, "https://imgur.com"),
                                 TextNode(" and some following text", TextType.TEXT),
                                 TextNode(" plus some bold", TextType.BOLD),
                                 TextNode("and another ", TextType.TEXT),
                                 TextNode("image", TextType.IMAGE, "https://imgur.com"),
                                 TextNode(" to follow", TextType.TEXT)
                             ])


    #Tests for extract markdown and extract links

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        matches = extract_markdown_images(
            "This line of markdown test includes two images, ![image one](https://paintbucket.net/image) and ![image two](https://imgur.com/rx580)"
        )
        self.assertListEqual([("image one", "https://paintbucket.net/image"), ("image two", "https://imgur.com/rx580")], matches)

    def test_extract_no_images(self):
        matches = extract_markdown_images(
            "This markdown text includes no images"
        )
        self.assertEqual(matches, [])

    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This text includes a [link](https://www.youtube.com/watch?v=dQw4w9WgXcQ)"
        )
        self.assertEqual(matches, [("link", "https://www.youtube.com/watch?v=dQw4w9WgXcQ")])

    def text_extract_multiple_links(self):
        matches = extract_markdown_links(
            "This one has [link one](boot.dev) and [link two](icy-veins.com)"
        )
        self.assertEqual(matches, [("link one", "boot.dev"), ("link two", "icy-veins.com")])

    def test_extract_no_links(self):
        matches = extract_markdown_links(
            "And finally, no links"
        )
        self.assertEqual(matches, [])

    def test_extract_empty_link(self):
        matches = extract_markdown_links(
            "This one has weird links []()"
        )
        self.assertEqual(matches, [("", "")])

    def test_extract_link_no_text(self):
        matches = extract_markdown_links(
            "This one is missing text [](myspace.com)"
        )
        self.assertEqual(matches, [("", "myspace.com")])

    #Tests for split_nodes_delimiter
    def test_italic(self):
        node = TextNode("This is a _text_ node", TextType.TEXT)
        new_node = split_nodes_delimiter(node, "_", TextType.ITALIC)
        self.assertEqual(new_node, [TextNode("This is a ", TextType.TEXT), TextNode("text", TextType.ITALIC), TextNode(" node", TextType.TEXT)])
    
    def test_bold(self):
        node = TextNode("This one is *bold* text", TextType.TEXT)
        new_node = split_nodes_delimiter(node, "*", TextType.BOLD)
        self.assertEqual(new_node, [TextNode("This one is ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode(" text", TextType.TEXT)])

    def test_delimiter_at_start(self):
        node = TextNode("*Bold text at the start* and then more regular text at the end", TextType.TEXT)
        new_node = split_nodes_delimiter(node, "*", TextType.BOLD)
        self.assertEqual(new_node, [TextNode("Bold text at the start", TextType.BOLD), TextNode(" and then more regular text at the end", TextType.TEXT)])

    def test_separated_delimiters(self):
        node = TextNode("This *statement* has more than one *bold* word", TextType.TEXT)
        new_node = split_nodes_delimiter(node, "*", TextType.BOLD)
        self.assertEqual(new_node, [TextNode("This ", TextType.TEXT), TextNode("statement", TextType.BOLD), TextNode(" has more than one ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode(" word", TextType.TEXT)] )

    def test_three_delimiters(self):
        node = TextNode("I _dont_ want _to_ write _this_ test", TextType.TEXT)
        new_node = split_nodes_delimiter(node, "_", TextType.ITALIC)
        self.assertEqual(new_node, [TextNode("I ", TextType.TEXT), TextNode("dont", TextType.ITALIC), TextNode(" want ", TextType.TEXT), TextNode("to", TextType.ITALIC), TextNode(" write ", TextType.TEXT), TextNode("this", TextType.ITALIC), TextNode(" test", TextType.TEXT)])

    def test_code(self):
        node = TextNode("I am writing some `code` in this function", TextType.TEXT)
        new_node = split_nodes_delimiter(node, "`", TextType.CODE)
        self.assertEqual(new_node, [TextNode("I am writing some ", TextType.TEXT), TextNode("code", TextType.CODE), TextNode(" in this function", TextType.TEXT)])

    def test_exception(self):
        node = TextNode("*This code should throw an error", TextType.TEXT)
        self.assertRaises(Exception, split_nodes_delimiter, node, "*", TextType.BOLD)

    def test_split_nodes_delimiter_mixed(self):
        node = [
            TextNode("Beginning *of* sentence ", TextType.TEXT),
            TextNode("already bold text", TextType.BOLD),
            TextNode(" ending *of* sentence", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(node, "*", TextType.BOLD)
        self.assertListEqual( new_nodes,
                             [
                                TextNode("Beginning ", TextType.TEXT),
                                TextNode("of", TextType.BOLD),
                                TextNode(" sentence ", TextType.TEXT),
                                TextNode("already bold text", TextType.BOLD),
                                TextNode(" ending ", TextType.TEXT),
                                TextNode("of", TextType.BOLD),
                                TextNode(" sentence", TextType.TEXT)
                             ])
    

if __name__ == "__main__":
    unittest.main()
