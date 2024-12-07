from enum import Enum
from htmlnode import LeafNode


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


    def to_html_leaf_node(self):
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
def split_text_nodes_on(text_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
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
