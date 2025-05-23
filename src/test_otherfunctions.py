import unittest

from otherfunctions import *
from textnode import *



class TestOtherFunctions(unittest.TestCase):

    #Tests for extract_title

    def test_extract_title(self):
        md = """
# Title of essay

Some more text

**Markdown stuff**
"""
        title = extract_title(md)
        self.assertEqual(title, "Title of essay")

    def test_extract_title_middle(self):
        md = """
Foreward: Four words included

# Title of **essay**

Appendix: You don't really need it
"""
        title = extract_title(md)
        self.assertEqual(title, "Title of **essay**")

    def test_extract_title_headers(self):
        md = """
## Some other second header, placed at the beginning for some reason.

# Why it's very annoying that VS code autofills the pound sign on newlines

Case in point
"""
        title = extract_title(md)
        self.assertEqual(title, "Why it's very annoying that VS code autofills the pound sign on newlines")

    #Tests for markdown_to_html_node and related helper functions

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headingblock(self):
        md = """
## Heading two
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual( html,
         "<div><h2>Heading two</h2></div>")
        
    def test_quoteblock(self):
        md = """
>On the guards' platform at Elsinore,
>Horatio waits with Barnardo and
>Marcellus to question a ghost that twice before appeared
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual( html,
                         "<div><blockquote>On the guards' platform at Elsinore,\nHoratio waits with Barnardo and\nMarcellus to question a ghost that twice before appeared</blockquote></div>")

    def test_unordered_list(self):
        md = """
- Get groceries
- Write code
- Go to bed
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual( html,
                         "<div><ul><li>Get groceries</li><li>Write code</li><li>Go to bed</li></ul></div>")
        
    def test_orderedlist(self):
        md = """
1. Get groceries
2. Write code
3. Go to bed
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual( html, 
                         "<div><ol><li>Get groceries</li><li>Write code</li><li>Go to bed</li></ol></div>")
        
    def test_inline_quote(self):
        md = """
>This quote has **bold**
>and _italic_ text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual( html,
            "<div><blockquote>This quote has <b>bold</b>\nand <i>italic</i> text</blockquote></div>")
        
    def test_inline_ul(self):
        md = """
- This list has **bold**
- and _italic_ text
- Even `code`
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual( html,
            "<div><ul><li>This list has <b>bold</b></li><li>and <i>italic</i> text</li><li>Even <code>code</code></li></ul></div>")
        
    def test_inline_ol(self):
        md = """
1. This list has **bold**
2. and _italic_ text
3. Even `code`
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual( html,
            "<div><ol><li>This list has <b>bold</b></li><li>and <i>italic</i> text</li><li>Even <code>code</code></li></ol></div>" )
        
    def test_inline_header(self):
        md = """
### A **bold** heading sans _italics_
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual( html,
            "<div><h3>A <b>bold</b> heading sans <i>italics</i></h3></div>")
        
    def test_heading_and_paragraph(self):
        md = """
# A **bold** heading

And a body of _text_ talking about `code`
probably some other stuff too
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual( html,
            "<div><h1>A <b>bold</b> heading</h1><p>And a body of <i>text</i> talking about <code>code</code> probably some other stuff too</p></div>")

    def test_three_blocks(self):
        md = """
## _Fancy_ Heading

>A quote from Shakespeare
>Something inspiring that
>Makes me look smart

And **finally** the recipe you've been scrolling
through this page looking for
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual( html,
            "<div><h2><i>Fancy</i> Heading</h2><blockquote>A quote from Shakespeare\nSomething inspiring that\nMakes me look smart</blockquote><p>And <b>finally</b> the recipe you've been scrolling through this page looking for</p></div>")
   
    #Tests for text_to_textnodes

    def test_text_to_textnodes(self):
        node = TextNode("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)", TextType.TEXT)
        new_nodes = text_to_textnodes(node)
        self.assertListEqual( new_nodes,
                             [
                            TextNode("This is ", TextType.TEXT),
                            TextNode("text", TextType.BOLD),
                            TextNode(" with an ", TextType.TEXT),
                            TextNode("italic", TextType.ITALIC),
                            TextNode(" word and a ", TextType.TEXT),
                            TextNode("code block", TextType.CODE),
                            TextNode(" and an ", TextType.TEXT),
                            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                            TextNode(" and a ", TextType.TEXT),
                            TextNode("link", TextType.LINK, "https://boot.dev"),
                             ])
        
    def test_text_to_textnodes_empty(self):
        node = TextNode("This node has no markdown text", TextType.TEXT)
        new_nodes = text_to_textnodes(node)
        self.assertEqual(new_nodes, [TextNode("This node has no markdown text", TextType.TEXT)])

    def test_text_to_textnodes_str(self):
        new_nodes = text_to_textnodes("This test passes **markdown** text without a _node_")
        self.assertListEqual( new_nodes,
                             [
                                 TextNode("This test passes ", TextType.TEXT),
                                 TextNode("markdown", TextType.BOLD),
                                 TextNode(" text without a ", TextType.TEXT),
                                 TextNode("node", TextType.ITALIC),
                                 #TextNode("", TextType.TEXT) #Ordering on function changed, no more trailing empty nodes
                             ])
        
    def test_text_to_textnodes_repeat(self):
        new_nodes = text_to_textnodes("This **test** reuses _some_ of the **same** _markdown_")
        self.assertListEqual( new_nodes,
                             [
                                 TextNode("This ", TextType.TEXT),
                                 TextNode("test", TextType.BOLD),
                                 TextNode(" reuses ", TextType.TEXT),
                                 TextNode("some", TextType.ITALIC),
                                 TextNode(" of the ", TextType.TEXT),
                                 TextNode("same", TextType.BOLD),
                                 TextNode(" ", TextType.TEXT),
                                 TextNode("markdown", TextType.ITALIC),
                                 #TextNode("", TextType.TEXT) #See _str
                             ])
        
    def test_text_to_textnodes_really_empty(self):
        new_nodes = text_to_textnodes("")
        self.assertEqual(new_nodes, [])

    def test_text_to_textnodes_multiple_images(self):
        new_nodes = text_to_textnodes("![image one](https://imgur.com) followed by a ![second image](https://paintbucket.com)")
        self.assertListEqual( new_nodes,
                             [
                                 TextNode("image one", TextType.IMAGE, "https://imgur.com"),
                                 TextNode(" followed by a ", TextType.TEXT),
                                 TextNode("second image", TextType.IMAGE, "https://paintbucket.com")
                             ])
        
    def test_text_to_textnodes_image_markdown(self):
        new_nodes = text_to_textnodes("![image one](https://imgur.com) and some **bold** text")
        self.assertListEqual( new_nodes,
                             [
                                 TextNode("image one", TextType.IMAGE, "https://imgur.com"),
                                 TextNode(" and some ", TextType.TEXT),
                                 TextNode("bold", TextType.BOLD),
                                 TextNode(" text", TextType.TEXT)
                             ])
        
    def test_text_to_textnodes_trailing_markdown(self):
        new_nodes = text_to_textnodes("This string has _trailing_ **markdown**")
        self.assertListEqual( new_nodes,
                             [
                                 TextNode("This string has ", TextType.TEXT),
                                 TextNode("trailing", TextType.ITALIC),
                                TextNode(" ", TextType.TEXT),
                                TextNode("markdown", TextType.BOLD)
                             ])
        
    def test_text_to_textnodes_trailing_mixed(self):
        new_nodes = text_to_textnodes("This string has [a link](https://website.com) and _trailing_ **markdown**")
        self.assertListEqual( new_nodes,
                             [
                                TextNode("This string has ", TextType.TEXT),
                                TextNode("a link", TextType.LINK, "https://website.com"),
                                TextNode(" and ", TextType.TEXT),
                                TextNode("trailing", TextType.ITALIC),
                                TextNode(" ", TextType.TEXT),
                                TextNode("markdown", TextType.BOLD)
                             ])
        
    def test_text_to_textnodes_leading(self):
        new_nodes = text_to_textnodes("**Bold beginning** to this markdown string")
        self.assertListEqual( new_nodes,
                             [
                                 TextNode("Bold beginning", TextType.BOLD),
                                 TextNode(" to this markdown string", TextType.TEXT)
                             ])

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
        node = TextNode("**Bold text at the start** and then more regular text at the end", TextType.TEXT)
        new_node = split_nodes_delimiter(node, "**", TextType.BOLD)
        self.assertEqual(new_node, [TextNode("", TextType.TEXT), TextNode("Bold text at the start", TextType.BOLD), TextNode(" and then more regular text at the end", TextType.TEXT)])

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

    """def test_exception(self): #Deprecated, no longer going one element at a time, split function will just return regular textnode when missing closing delimiter
        node = TextNode("*This code should throw an error", TextType.TEXT)
        self.assertRaises(Exception, split_nodes_delimiter, node, "*", TextType.BOLD)"""

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
