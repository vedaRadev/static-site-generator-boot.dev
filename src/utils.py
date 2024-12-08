import re
from functools import reduce


def extract_markdown_images(md_text: str) -> list[tuple[str, str]]:
    result = []
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", md_text)
    for match in matches:
        result.append((match[0], match[1]))

    return matches


def extract_markdown_links(md_text: str) -> list[tuple[str, str]]:
    result = []
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", md_text)
    for match in matches:
        result.append((match[0], match[1]))

    return matches


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


# NOTE exepcts ONE title per invocation
# TODO Was accidentally looking at the wrong lesson but I'll go ahead and make note of the regex I
# constructed for this: ^\s*\#\s*(.*?(\n|\r\n))
def extract_title(md_text: str) -> str:
    pass
