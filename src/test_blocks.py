import unittest

from blocks import *


class TestBlocks(unittest.TestCase):
    #Tests for block_to_blocktype

    def test_block_to_blocktype_heading(self):
        block_type = block_to_block_type("#. Heading one")
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_blocktype_multiple_headings(self):
        block_type = block_to_block_type("#. Heading one\n##. Heading two\n###. Heading three")
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_blocktype_code(self):
        block_type = block_to_block_type("```Code block```")
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_blocktype_codes(self):
        block_type = block_to_block_type("```A longer\nCode block\nIncluded```")
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_blocktype_quote(self):
        block_type = block_to_block_type(">Two households, both alike in dignity\n>In fair Verona, where we lay our scene\n>From ancient grudge break to new mutiny")
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_blocktype_unordered_list(self):
        block_type = block_to_block_type("- Buy groceries\n- Do laundry\n- Wash dishes\n- Finish SSG")
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_blocktype_ordered_list(self):
        block_type = block_to_block_type("1. Learn to count\n2. Learn to read\n3. Learn to code")
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_to_blocktype_empty(self):
        block_type = block_to_block_type("")
        self.assertEqual(block_type, BlockType.PARAGRAPH)


    #Tests for markdown_to_blocks

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_extra_newlines(self):
        md = """
Testing a paragraph


with an extra set of newlines.

End"""
        blocks = markdown_to_blocks(md)
        self.assertEqual( blocks,
                         [
                             "Testing a paragraph",
                             "with an extra set of newlines.",
                             "End"
                         ])
        
    def test_markdown_to_blocks_leading_newlines(self):
        md = """



Leading newlines.


And more of them"""
        blocks = markdown_to_blocks(md)
        self.assertEqual( blocks,
                         [
                             "Leading newlines.",
                             "And more of them"
                         ])
        
    def test_markdown_to_blocks_leading_whitespace(self):
        md = """
       This block has some leading whitespace.

       And trailing too       """
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks,
                         [
                             "This block has some leading whitespace.",
                             "And trailing too"
                         ])

    def test_markdown_to_blocks_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

if __name__ == "__main__":
    unittest.main()
