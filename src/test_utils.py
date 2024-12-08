import unittest
from utils import extract_markdown_images, extract_markdown_links


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
