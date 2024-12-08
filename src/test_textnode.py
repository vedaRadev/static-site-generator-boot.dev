import unittest

from textnode import TextNode, TextType
from textnode import split_text_nodes_on_delimiter, split_text_nodes_on_image, split_text_nodes_on_link

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


class TestTextNodeDelimiterSplitting(unittest.TestCase):
    def test_simple(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_text_nodes_on_delimiter([node], "`", TextType.CODE)

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
            split_text_nodes_on_delimiter([node], "*", TextType.BOLD)


    def test_multiple(self):
        node1 = TextNode("there _are_ some _delimited_ words", TextType.NORMAL)
        node2 = TextNode("and _some_ here _too__test_", TextType.NORMAL)
        new_nodes = split_text_nodes_on_delimiter([node1, node2], "_", TextType.ITALIC)

        self.assertEqual(len(new_nodes), 10)
        italic_nodes = list(filter(lambda node: node.text_type == TextType.ITALIC, new_nodes))
        self.assertEqual(5, len(italic_nodes))
        for italic_node in italic_nodes:
            self.assertNotIn("_", italic_node.text)


    def test_triple_delimiter(self):
        node1 = TextNode("this is a ```triple``` delimiter", TextType.NORMAL)
        new_nodes = split_text_nodes_on_delimiter([node1], "```", TextType.CODE)

        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(1, len(list(filter(lambda node: node.text_type == TextType.CODE, new_nodes))))
        self.assertNotIn("```", new_nodes[1].text)


class TestTextNodeLinkSplitting(unittest.TestCase):
    def test_single_lone_link(self):
        node = TextNode("[link](www.link.com)", TextType.NORMAL)
        result = split_text_nodes_on_link([ node ])
        self.assertListEqual(
            result,
            [ TextNode("link", TextType.LINK, "www.link.com") ],
        )


    def test_multiple_lone_links(self):
        node1 = TextNode("[link #1](www.link1.com)", TextType.NORMAL)
        node2 = TextNode("[link #2](www.link2.com)", TextType.NORMAL)
        node3 = TextNode("[link #3](www.link3.com)", TextType.NORMAL)
        node4 = TextNode("[link #4](www.link4.com)", TextType.NORMAL)
        result = split_text_nodes_on_link([ node1, node2, node3, node4 ])
        self.assertListEqual(
            result,
            [
                TextNode("link #1", TextType.LINK, "www.link1.com"),
                TextNode("link #2", TextType.LINK, "www.link2.com"),
                TextNode("link #3", TextType.LINK, "www.link3.com"),
                TextNode("link #4", TextType.LINK, "www.link4.com"),
            ],
        )


    def test_multiple_links_one_line(self):
        node = TextNode("[link a](www.link_a.com) followed by [link b](www.link_b.com)", TextType.NORMAL)
        result = split_text_nodes_on_link([ node ])
        self.assertListEqual(
            result,
            [
                TextNode("link a", TextType.LINK, "www.link_a.com"),
                TextNode(" followed by ", TextType.NORMAL),
                TextNode("link b", TextType.LINK, "www.link_b.com"),
            ],
        )


    def test_many_with_multiple_lines(self):
        node1 = TextNode("[link a](www.link_a.com) followed by [link b](www.link_b.com)", TextType.NORMAL)
        node2 = TextNode("start [link c](www.link_c.com) followed by [link d](www.link_d.com) end", TextType.NORMAL)
        result = split_text_nodes_on_link([ node1, node2 ])
        self.assertListEqual(
            result,
            [
                TextNode("link a", TextType.LINK, "www.link_a.com"),
                TextNode(" followed by ", TextType.NORMAL),
                TextNode("link b", TextType.LINK, "www.link_b.com"),
                TextNode("start ", TextType.NORMAL),
                TextNode("link c", TextType.LINK, "www.link_c.com"),
                TextNode(" followed by ", TextType.NORMAL),
                TextNode("link d", TextType.LINK, "www.link_d.com"),
                TextNode(" end", TextType.NORMAL),
            ],
        )


class TestTextNodeImageSplitting(unittest.TestCase):
    def test_single_lone_image(self):
        node = TextNode("![image](./res/img/image.jpg)", TextType.NORMAL)
        result = split_text_nodes_on_image([ node ])
        self.assertListEqual(
            result,
            [ TextNode("image", TextType.IMAGE, "./res/img/image.jpg") ],
        )


    def test_multiple_lone_images(self):
        node1 = TextNode("![image #1](./res/img/image1.jpg)", TextType.NORMAL)
        node2 = TextNode("![image #2](./res/img/image2.jpg)", TextType.NORMAL)
        node3 = TextNode("![image #3](./res/img/image3.jpg)", TextType.NORMAL)
        node4 = TextNode("![image #4](./res/img/image4.jpg)", TextType.NORMAL)
        result = split_text_nodes_on_image([ node1, node2, node3, node4 ])
        self.assertListEqual(
            result,
            [
                TextNode("image #1", TextType.IMAGE, "./res/img/image1.jpg"),
                TextNode("image #2", TextType.IMAGE, "./res/img/image2.jpg"),
                TextNode("image #3", TextType.IMAGE, "./res/img/image3.jpg"),
                TextNode("image #4", TextType.IMAGE, "./res/img/image4.jpg"),
            ],
        )


    def test_multiple_images_one_line(self):
        node = TextNode("![image a](./res/img/image_a.jpg) followed by ![image b](./res/img/image_b.jpg)", TextType.NORMAL)
        result = split_text_nodes_on_image([ node ])
        self.assertListEqual(
            result,
            [
                TextNode("image a", TextType.IMAGE, "./res/img/image_a.jpg"),
                TextNode(" followed by ", TextType.NORMAL),
                TextNode("image b", TextType.IMAGE, "./res/img/image_b.jpg"),
            ],
        )


    def test_many_with_multiple_lines(self):
        node1 = TextNode("![image a](./res/img/image_a.jpg) followed by ![image b](./res/img/image_b.jpg)", TextType.NORMAL)
        node2 = TextNode("start ![image c](./res/img/image_c.jpg) followed by ![image d](./res/img/image_d.jpg) end", TextType.NORMAL)
        result = split_text_nodes_on_image([ node1, node2 ])
        self.assertListEqual(
            result,
            [
                TextNode("image a", TextType.IMAGE, "./res/img/image_a.jpg"),
                TextNode(" followed by ", TextType.NORMAL),
                TextNode("image b", TextType.IMAGE, "./res/img/image_b.jpg"),
                TextNode("start ", TextType.NORMAL),
                TextNode("image c", TextType.IMAGE, "./res/img/image_c.jpg"),
                TextNode(" followed by ", TextType.NORMAL),
                TextNode("image d", TextType.IMAGE, "./res/img/image_d.jpg"),
                TextNode(" end", TextType.NORMAL),
            ],
        )
