from markdown_to_html import markdown_to_html

def main():
    text = "This is **bold** text _in_ a paragraph"
    print(markdown_to_html(text).to_html())

if __name__ == "__main__":
    main()
