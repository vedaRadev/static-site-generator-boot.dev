from utils import extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType, split_text_nodes_on_link, split_text_nodes_on_image

def main():
    node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.NORMAL,
    )

    result = split_text_nodes_on_link([node])
    print(result)

if __name__ == "__main__":
    main()
