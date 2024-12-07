import unittest

from textnode import TextNode, TextType
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node1, node2)

        node1 = TextNode("This is a text node", TextType.IMAGE)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertNotEqual(node1, node2)


    def test_repr(self):
        url = "boot.dev"
        text = "This is a text node"
        text_type = TextType.BOLD
        node = TextNode(text, text_type, url)
        self.assertEqual(f"{node}", f"TextNode({text}, {text_type.value}, {url})")


    def test_to_leafnode_normal(self):
        textnode = TextNode("normal", TextType.NORMAL)
        leafnode = textnode.to_html_leaf_node()
        self.assertIsInstance(leafnode, LeafNode)
        html = leafnode.to_html()
        self.assertEqual(
            html,
            textnode.text
        )


    def test_to_leafnode_bold(self):
        textnode = TextNode("bold", TextType.BOLD)
        leafnode = textnode.to_html_leaf_node()
        self.assertIsInstance(leafnode, LeafNode)
        html = leafnode.to_html()
        self.assertEqual(
            html,
            f"<b>{textnode.text}</b>"
        )


    def test_to_leafnode_italic(self):
        textnode = TextNode("italic", TextType.ITALIC)
        leafnode = textnode.to_html_leaf_node()
        self.assertIsInstance(leafnode, LeafNode)
        html = leafnode.to_html()
        self.assertEqual(
            html,
            f"<i>{textnode.text}</i>"
        )


    def test_to_leafnode_code(self):
        textnode = TextNode("code", TextType.CODE)
        leafnode = textnode.to_html_leaf_node()
        self.assertIsInstance(leafnode, LeafNode)
        html = leafnode.to_html()
        self.assertEqual(
            html,
            f"<code>{textnode.text}</code>"
        )


    def test_to_leafnode_link(self):
        textnode = TextNode("a", TextType.LINK)
        leafnode = textnode.to_html_leaf_node()
        self.assertIsInstance(leafnode, LeafNode)
        html = leafnode.to_html()
        self.assertEqual(
            html,
            f'<a href="{textnode.url}">{textnode.text}</a>'
        )


    def test_to_leafnode_image(self):
        textnode = TextNode("img", TextType.IMAGE)
        leafnode = textnode.to_html_leaf_node()
        self.assertIsInstance(leafnode, LeafNode)
        html = leafnode.to_html()
        self.assertEqual(
            html,
            f'<img src="{textnode.url}" alt="{textnode.text}"></img>'
        )
