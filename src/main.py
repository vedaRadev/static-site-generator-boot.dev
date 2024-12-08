from textnode import TextNode, TextType, to_text_nodes

def main():
    result = to_text_nodes("This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")

if __name__ == "__main__":
    main()
