from utils import extract_markdown_images

def main():
    matches = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
    print(matches[0][1])

if __name__ == "__main__":
    main()
