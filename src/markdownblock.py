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


def block_reducer(acc: list[str], line: str) -> list[str]:
    # is the line all whitespace?
    if not "".join(line.split()):
        # avoid runs of empty strings in the acc
        if acc and acc[-1]:
            acc.append("")
    else:
        if len(acc) == 0:
            acc.append("")
        acc[-1] += ("\n" if acc[-1] else "") + line.strip("\t ")
    return acc


def markdown_to_blocks(md_document: str) -> list[str]:
    result = reduce(block_reducer, md_document.splitlines(), [])
    # If there is a line of whitespace at the end of the string we'll end up with a trailing newline
    return result if not result or result[-1] else result[0:-1]


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


