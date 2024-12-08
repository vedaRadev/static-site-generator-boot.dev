from utils import markdown_to_blocks

def main():
    string = """# This is a heading
                
This is a paragraph of text. It has some **bold** and *italic* words inside of it.
    
* This is the first list item in a list block    
* This is a list item
* This is another list item
    """

    # print(string.splitlines())
    print(markdown_to_blocks(string))

if __name__ == "__main__":
    main()
