import unittest
from markdownblock import BlockType, markdown_to_blocks, block_to_block_type


class TestMarkdownBlockExtractor(unittest.TestCase):
    def test_empty_string(self):
        result = markdown_to_blocks("")
        self.assertListEqual(result, [])

    
    def test_all_whitespace(self):
        result = markdown_to_blocks("\n\n    \t\n \r\n")
        self.assertListEqual(result, [])


    def test_single_title(self):
        result = markdown_to_blocks("# Simple")
        self.assertListEqual(result, [ "# Simple" ])


    def test_unordered_list(self):
        text = "* Apples\n* Eggs\n* Cheese\n* Grapes\n* Wine"
        result = markdown_to_blocks(text)
        self.assertListEqual(result, [ text ])


    def test_strips_trailing_whitespace(self):
        text = "First block\n\n\n\nSecond block\n\n\n\n"
        result = markdown_to_blocks(text)
        self.assertListEqual(result, [ "First block", "Second block" ])


    def test_ignores_leading_whitespace_lines(self):
        text = "\n    \n\n   \t   \nBlock"
        result = markdown_to_blocks(text)
        self.assertListEqual(result, [ "Block" ])


    def test_strips_leading_whitespace_from_blocks(self):
        text = "       Leading whitespace\n\n      Here too"
        result = markdown_to_blocks(text)
        self.assertListEqual(result, [ "Leading whitespace", "Here too" ])


    def test_quote_real_world_example_unquote(self):
        text = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* First
* Second
* Third
        """
        result = markdown_to_blocks(text)
        self.assertListEqual(
            result,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* First\n* Second\n* Third"
            ]
        )


class TestMarkdownBlockToBlockType(unittest.TestCase):
    def test_simple_paragraph(self):
        text = "This is just a paragraph"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.PARAGRAPH)


    def test_malformed_quote_is_paragraph(self):
        text = "> I look like a quote\n> Sound like a quote\nBut I'm not"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.PARAGRAPH)


    def test_malformed_unordered_list_is_paragraph(self):
        text = "* I look like a UL\n- Sound like a UL\nBut I'm not"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    
    def test_malformed_ordered_list_is_paragraph(self):
        text = "1. Good start\n2. Still going strong\n4. Oops, missed a number"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.PARAGRAPH)


    def test_malformed_code_block_is_paragraph(self):
        text = "```I don't terminate properly"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.PARAGRAPH)


    def test_malformed_header_is_paragraph(self):
        # 7 #'s, max is 6
        text = "#######"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.PARAGRAPH)


    def test_code_block(self):
        text = "```This is a code block\nmore code\neven more code```"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.CODE)


    def test_heading(self):
        text = "# Header"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.HEADING)

        text = "## Header"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.HEADING)

        text = "### Header"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.HEADING)

        text = "#### Header"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.HEADING)

        text = "##### Header"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.HEADING)

        text = "###### Header"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.HEADING)


    def test_unordered_list(self):
        text = "* a\n- b\n* c\n- d"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)


    def test_ordered_list(self):
        text = "1. 1\n2. 2\n3. 3\n4. 4\n5. 5\n6. 6\n7. 7\n8. 8\n9. 9\n10. 10"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    
    def test_quote(self):
        text = "> a\n> b\n> c\n"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.QUOTE)
