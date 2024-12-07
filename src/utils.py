import re


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    result = []
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    for match in matches:
        result.append((match[0], match[1]))

    return matches


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    result = []
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    for match in matches:
        result.append((match[0], match[1]))

    return matches
