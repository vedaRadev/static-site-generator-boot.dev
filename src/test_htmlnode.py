import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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


class TestHTMLParentNode(unittest.TestCase):
    def test_no_children(self):
        node = ParentNode("a", None)
        self.assertRaises(ValueError, node.to_html)

        node = ParentNode("a", [])
        self.assertRaises(ValueError, node.to_html)


    def test_no_tag(self):
        node = ParentNode(None, [ HTMLNode() ])
        self.assertRaises(ValueError, node.to_html)


    def test_simple(self):
        node = ParentNode(
            "div",
            [
                LeafNode("p", "paragraph"),
                LeafNode("b", "bold"),
                LeafNode(None, "normal"),
            ]
        )

        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>paragraph</p><b>bold</b>normal</div>"
        )


    def test_nested(self):
        node = ParentNode(
            "div",
            [
                LeafNode("p", "paragraph"),
                ParentNode(
                    "span",
                    [
                        LeafNode("i", "italic"),
                        LeafNode("a", "link", { "href": "google.com" }),
                        LeafNode(None, "normal")
                    ],
                ),
                LeafNode(None, "normal"),
            ]
        )

        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>paragraph</p><span><i>italic</i><a href="google.com">link</a>normal</span>normal</div>'
        )
