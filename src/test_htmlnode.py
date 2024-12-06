import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(value = "whatever", props = { "href": "google.com", "target": "_blank" })
        html_attribs = node.props_to_html()
        self.assertEqual(' href="google.com" target="_blank"', html_attribs)
