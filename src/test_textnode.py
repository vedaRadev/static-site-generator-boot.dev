import unittest

from textnode import TextNode, TextType, split_text_nodes_on
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


class TestTextNodeUtils(unittest.TestCase):
    def test_simple(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_text_nodes_on([node], "`", TextType.CODE)

        self.assertEqual(len(new_nodes), 3)

        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text_type, TextType.NORMAL)

        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[2].text, " word")

        self.assertNotIn("`", new_nodes[1].text)
    

    def test_invalid_markdown(self):
        node = TextNode("unterminated *delimiter", TextType.NORMAL)
        with self.assertRaises(ValueError):
            split_text_nodes_on([node], "*", TextType.BOLD)


    def test_multiple(self):
        node1 = TextNode("there _are_ some _delimited_ words", TextType.NORMAL)
        node2 = TextNode("and _some_ here _too__test_", TextType.NORMAL)
        new_nodes = split_text_nodes_on([node1, node2], "_", TextType.ITALIC)

        self.assertEqual(len(new_nodes), 10)
        italic_nodes = list(filter(lambda node: node.text_type == TextType.ITALIC, new_nodes))
        self.assertEqual(5, len(italic_nodes))
        for italic_node in italic_nodes:
            self.assertNotIn("_", italic_node.text)


    def test_triple_delimiter(self):
        node1 = TextNode("this is a ```triple``` delimiter", TextType.NORMAL)
        new_nodes = split_text_nodes_on([node1], "```", TextType.CODE)

        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(1, len(list(filter(lambda node: node.text_type == TextType.CODE, new_nodes))))
        self.assertNotIn("```", new_nodes[1].text)
