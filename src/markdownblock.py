from enum import Enum
from functools import reduce
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(md_document: str) -> list[str]:
    blocks = md_document.split("\n\n")
    filtered = []
    for block in blocks:
        block = block.strip()
        if not block: continue
        filtered.append(block)

    return filtered


def is_quote_item(s: str) -> bool:
    return s.startswith(">")

def is_unordered_list_item(s: str) -> bool:
    return s.startswith("* ") or s.startswith("- ")

def block_to_block_type(block: str) -> BlockType:
    if re.match(r"^\#{1,6}\s.*", block):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    if is_quote_item(block):
        if all(is_quote_item(line) for line in block.splitlines()):
            return BlockType.QUOTE
    elif is_unordered_list_item(block):
        if all(is_unordered_list_item(line) for line in block.splitlines()):
            return BlockType.UNORDERED_LIST
    elif block.startswith("1. "):
        is_valid_ordered_list_block = True
        expected_item_number = 1
        for line in block.splitlines():
            match = re.match(r"^(\d+)\.", line)
            if not match or int(match.group(1)) != expected_item_number:
                is_valid_ordered_list_block = False
                break
            expected_item_number += 1

        if is_valid_ordered_list_block:
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


