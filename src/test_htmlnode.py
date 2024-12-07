import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(value = "whatever", props = { "href": "google.com", "target": "_blank" })
        html_attribs = node.props_to_html()
        self.assertEqual(' href="google.com" target="_blank"', html_attribs)


class TestHTMLLeafNode(unittest.TestCase):
    def test_with_value(self):
        leaf_node = LeafNode("a", "google.com", { "prop1": "prop1", "prop2": "prop2" })
        leaf_node_html = leaf_node.to_html()
        self.assertEqual(leaf_node_html, '<a prop1="prop1" prop2="prop2">google.com</a>')

    def test_with_no_value(self):
        leaf_node = LeafNode("a", None, { "prop1": "prop1", "prop2": "prop2" })
        self.assertRaises(ValueError, leaf_node.to_html)
