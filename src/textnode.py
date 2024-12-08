from enum import Enum
from htmlnode import LeafNode
from utils import extract_markdown_links, extract_markdown_images
from typing import Callable


class TextType(Enum):
    NORMAL  = "normal"
    BOLD    = "bold"
    ITALIC  = "italic"
    CODE    = "code"
    LINK    = "link"
    IMAGE   = "image"


class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url


    def __eq__(self, other):
        return (self.text == other.text
                and self.text_type == other.text_type
                and self.url == other.url)


    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


    def to_html_leaf_node(self) -> LeafNode:
        match self.text_type:
            case TextType.NORMAL:
                return LeafNode(None, self.text)
            case TextType.BOLD:
                return LeafNode("b", self.text);
            case TextType.ITALIC:
                return LeafNode("i", self.text);
            case TextType.CODE:
                return LeafNode("code", self.text);
            case TextType.LINK:
                return LeafNode("a", self.text, { "href": self.url });
            case TextType.IMAGE:
                return LeafNode("img", "", { "src": self.url, "alt": self.text })
        raise Exception("unknown text type")


# NOTE At the moment we're not supported nested delimiters.
# e.g. "This is an *italic and **bold** word*" is NOT supported.
# TODO Rename to split_text_nodes_on_delimiter
def split_text_nodes_on_delimiter(text_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    """
    Return a new list of text nodes. The original list is split on the delimiter and the new node
    types are of text_type. Nested delimiters is not supported. Only supports splitting on NORMAL
    text_type nodes.
    """
    new_nodes = []
    for node in text_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        split_text = node.text.split(delimiter)
        # "invalid * markdown" => ["invalid", "markdown"]
        # "valid *markdown* here" => ["valid", "markdown", "here"]
        # "valid markdown *here*" => ["valid markdown ", "here", ""]
        if len(split_text) % 2 == 0:
            raise ValueError("invalid markdown: unterminated delimiter")

        # delimiter not found in node
        if len(split_text) == 1:
            new_nodes.append(node)
            continue

        # text wrapped by the delimiter should only occur at the _odd_ indices
        for i in range(0, len(split_text)):
            text = split_text[i]

            # ignore empty string
            if not text:
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(text, node.text_type, node.url))
            else:
                new_nodes.append(TextNode(text, text_type, node.url))

    return new_nodes


# TODO this might not be a great name for the function since it's dealing mostly with just images
# and links
def split_text_nodes_on_markdown_element(
    text_nodes: list[TextNode],
    md_extractor: Callable[[str], list[tuple[str, str]]],
    to_delimiter: Callable[[str, str], str],
    text_type: TextType
) -> list[TextNode]:
    new_text_nodes = []

    for node in text_nodes:
        matches = md_extractor(node.text)
        if not matches:
            new_text_nodes.append(node)
            continue

        after = node.text
        for text, url in matches:
            delimiter = to_delimiter(text, url)
            before, after = after.split(delimiter, 1)
            if before:
                new_text_nodes.append(TextNode(before, node.text_type, node.url))
            new_text_nodes.append(TextNode(text, text_type, url))
        
        # there was additional stuff left over that we need to account for
        if after:
            new_text_nodes.append(TextNode(after, node.text_type, node.url))

    return new_text_nodes


def split_text_nodes_on_link(text_nodes: list[TextNode]) -> list[TextNode]:
    return split_text_nodes_on_markdown_element(
        text_nodes,
        extract_markdown_links,
        lambda href, url: f"[{href}]({url})",
        TextType.LINK
    )


def split_text_nodes_on_image(text_nodes: list[TextNode]) -> list[TextNode]:
    return split_text_nodes_on_markdown_element(
        text_nodes,
        extract_markdown_images,
        lambda href, url: f"![{href}]({url})",
        TextType.IMAGE
    )


# FIXME This is probably very inefficient
def to_text_nodes(text: str) -> list[TextNode]:
    nodes = [ TextNode(text, TextType.NORMAL) ]
    instructions = [
        lambda nodes: split_text_nodes_on_delimiter(nodes, "**", TextType.BOLD),
        lambda nodes: split_text_nodes_on_delimiter(nodes, "__", TextType.BOLD),
        lambda nodes: split_text_nodes_on_delimiter(nodes, "*", TextType.ITALIC),
        lambda nodes: split_text_nodes_on_delimiter(nodes, "_", TextType.ITALIC),
        lambda nodes: split_text_nodes_on_delimiter(nodes, "`", TextType.CODE),
        split_text_nodes_on_image,
        split_text_nodes_on_link,
    ]

    for instruction in instructions:
        nodes = instruction(nodes)

    return nodes
