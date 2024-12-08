import re


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


# NOTE exepcts ONE title per invocation
# TODO Was accidentally looking at the wrong lesson but I'll go ahead and make note of the regex I
# constructed for this: ^\s*\#\s*(.*?(\n|\r\n))
def extract_title(md_text: str) -> str:
    pass
