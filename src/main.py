from textnode import TextNode, TextType, split_text_nodes_on

def main():
    pass

if __name__ == "__main__":
    node = TextNode("This is text with a `code block` word", TextType.NORMAL)
    new_nodes = split_text_nodes_on([node], "`", TextType.CODE)
    print(new_nodes)
