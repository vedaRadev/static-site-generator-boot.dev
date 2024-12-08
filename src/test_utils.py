import unittest
from utils import extract_markdown_images, extract_markdown_links, markdown_to_blocks


class TestMarkdownImageExtraction(unittest.TestCase):
    def test_simple(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0][0], "rick roll")
        self.assertEqual(matches[0][1], "https://i.imgur.com/aKaOqIh.gif")
        self.assertEqual(matches[1][0], "obi wan")
        self.assertEqual(matches[1][1], "https://i.imgur.com/fJRm4Vk.jpeg")


class TestMarkdownLinkExtraction(unittest.TestCase):
    def test_simple(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0][0], "to boot dev")
        self.assertEqual(matches[0][1], "https://www.boot.dev")
        self.assertEqual(matches[1][0], "to youtube")
        self.assertEqual(matches[1][1], "https://www.youtube.com/@bootdotdev")


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
