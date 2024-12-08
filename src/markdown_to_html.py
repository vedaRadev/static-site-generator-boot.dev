from htmlnode import HTMLNode, ParentNode, LeafNode
from markdownblock import BlockType, markdown_to_blocks, block_to_block_type
from textnode import to_text_nodes
import re

def markdown_to_html(md_doc: str) -> HTMLNode:
    html_children = []

    blocks = markdown_to_blocks(md_doc)
    for block in blocks:
        html_node = None

        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                text_nodes = to_text_nodes(block)
                for node in text_nodes:
                    node.text = node.text.replace("\n", " ")
                html_node = ParentNode("p", list(map(lambda tn: tn.to_html_leaf_node(), text_nodes)))

            case BlockType.HEADING:
                heading_level = len(re.match(r"^\#{1,6}", block).group(0)) # type: ignore
                text_nodes = to_text_nodes(block.lstrip("#").strip())
                html_node = ParentNode(f"h{heading_level}", list(map(lambda tn: tn.to_html_leaf_node(), text_nodes)))

            case BlockType.CODE:
                html_node = ParentNode("pre", [ ParentNode("code", [ LeafNode(None, block.strip("```").strip()) ]) ])

            case BlockType.QUOTE:
                # > quote line
                # > quote line
                # > quote line
                # 
                # becomes
                #
                # <blockquote>quote line quote line quote line</blockquote>
                gt_stripped = " ".join(map(lambda s: s.lstrip('>').lstrip(), block.splitlines()))
                text_nodes = to_text_nodes(gt_stripped)
                html_node = ParentNode("blockquote", list(map(lambda tn: tn.to_html_leaf_node(), text_nodes)))

            case BlockType.UNORDERED_LIST:
                temp = map(lambda line: line[2:], block.splitlines()) # strip leading "- " or "* "
                temp = map(to_text_nodes, temp)
                temp = map(lambda text_nodes: map(lambda tn: tn.to_html_leaf_node(), text_nodes), temp)
                temp = map(lambda leaves: ParentNode("li", list(leaves)), temp)
                html_node = ParentNode("ul", list(temp))

            case BlockType.ORDERED_LIST:
                temp = map(lambda line: re.sub(r"^\d+\. ", "", line.strip()), block.splitlines()) # strip leading numbers
                temp = map(to_text_nodes, temp)
                temp = map(lambda text_nodes: map(lambda tn: tn.to_html_leaf_node(), text_nodes), temp)
                temp = map(lambda leaves: ParentNode("li", list(leaves)), temp)
                html_node = ParentNode("ol", list(temp))

        html_children.append(html_node)

    return ParentNode("div", html_children)
