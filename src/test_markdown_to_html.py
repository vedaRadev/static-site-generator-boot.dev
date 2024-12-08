import unittest
from markdown_to_html import markdown_to_html
from htmlnode import LeafNode, ParentNode

class TestMarkdownToHtml(unittest.TestCase):
    def test_single_paragraph(self):
        text = "this is a paragraph"
        result = markdown_to_html(text)
        self.assertEqual(
            result,
            ParentNode(
                "div",
                [ ParentNode("p", [ LeafNode(None, text) ]) ]
            )
        )


    def test_single_paragraph_multiline(self):
        text = "this is a paragraph\nnewlines should become spaces"
        result = markdown_to_html(text)
        self.assertEqual(
            result,
            ParentNode(
                "div",
                [ ParentNode("p", [ LeafNode(None, "this is a paragraph newlines should become spaces") ]) ]
            )
        )


    def test_multiple_paragraph(self):
        text = "paragraph 1\n\nparagraph 2\n\nparagraph 3"
        result = markdown_to_html(text)
        self.assertEqual(
            result,
            ParentNode(
                "div",
                [
                    ParentNode("p", [ LeafNode(None, "paragraph 1") ]),
                    ParentNode("p", [ LeafNode(None, "paragraph 2") ]),
                    ParentNode("p", [ LeafNode(None, "paragraph 3") ]),
                ]
            )
        )

    
    def test_unordered_list(self):
        text = "* item 1\n* item 2\n* item 3"
        result = markdown_to_html(text)
        self.assertEqual(
            result,
            ParentNode(
                "div",
                [
                    ParentNode(
                        "ul",
                        [
                            ParentNode("li", [ LeafNode(None, "item 1") ]),
                            ParentNode("li", [ LeafNode(None, "item 2") ]),
                            ParentNode("li", [ LeafNode(None, "item 3") ]),
                        ]
                    )
                ]
            )
        )
    

    def test_ordered_list(self):
        text = "1. item 1\n2. item 2\n3. item 3"
        result = markdown_to_html(text)
        self.assertEqual(
            result,
            ParentNode(
                "div",
                [
                    ParentNode(
                        "ol",
                        [
                            ParentNode("li", [ LeafNode(None, "item 1") ]),
                            ParentNode("li", [ LeafNode(None, "item 2") ]),
                            ParentNode("li", [ LeafNode(None, "item 3") ]),
                        ]
                    )
                ]
            )
        )


    def test_headings(self):
        text = "# heading"
        result = markdown_to_html(text)
        self.assertEqual(
            result,
            ParentNode(
                "div",
                [ ParentNode("h1", [ LeafNode(None, "heading") ]) ]
            )
        )

        text = "## heading"
        result = markdown_to_html(text)
        self.assertEqual(
            result,
            ParentNode(
                "div",
                [ ParentNode("h2", [ LeafNode(None, "heading") ]) ]
            )
        )

        text = "### heading"
        result = markdown_to_html(text)
        self.assertEqual(
            result,
            ParentNode(
                "div",
                [ ParentNode("h3", [ LeafNode(None, "heading") ]) ]
            )
        )

        text = "#### heading"
        result = markdown_to_html(text)
        self.assertEqual(
            result,
            ParentNode(
                "div",
                [ ParentNode("h4", [ LeafNode(None, "heading") ]) ]
            )
        )

        text = "##### heading"
        result = markdown_to_html(text)
        self.assertEqual(
            result,
            ParentNode(
                "div",
                [ ParentNode("h5", [ LeafNode(None, "heading") ]) ]
            )
        )

        text = "###### heading"
        result = markdown_to_html(text)
        self.assertEqual(
            result,
            ParentNode(
                "div",
                [ ParentNode("h6", [ LeafNode(None, "heading") ]) ]
            )
        )

    
    def test_code(self):
        text = "this is a code block with **bold** that shouldn't be parsed"
        code = f"```{text}```" 
        result = markdown_to_html(code)
        self.assertEqual(
            result,
            ParentNode(
                "div",
                [
                    ParentNode(
                        "pre",
                        [
                            ParentNode("code", [ LeafNode(None, text) ])
                        ]
                    )
                ]
            )
        )


    def test_quote(self):
        text = "> line 1\n> line 2\n> line 3"
        result = markdown_to_html(text)
        self.assertEqual(
            result,
            ParentNode(
                "div",
                [
                    ParentNode(
                        "blockquote",
                        [ LeafNode(None, "line 1 line 2 line 3") ]
                    )
                ]
            )
        )


    def test_big(self):
        text = """
        # MY MARKDOWN DOCUMENT
        
        ## _Italic Section_

        1. Apples
        2. Cheese
        3. Wine

        - [google](google.com)
        - [netflix](netflix.com)

        ```
        Not sure what to type here.
        Second line.
        [link](link.com)
        ```

        > **bolded quote** with `inline code`

        ### ![my image](./img.jpg)

        Regular paragraph.
        Should be on same line.
        """
        result = markdown_to_html(text)
        self.assertEqual(
            result,
            ParentNode(
                "div",
                [
                    ParentNode("h1", [ LeafNode(None, "MY MARKDOWN DOCUMENT") ]),
                    ParentNode("h2", [ LeafNode("i", "Italic Section") ]),
                    ParentNode(
                        "ol",
                        [
                            ParentNode("li", [ LeafNode(None, "Apples") ]),
                            ParentNode("li", [ LeafNode(None, "Cheese") ]),
                            ParentNode("li", [ LeafNode(None, "Wine") ]),
                        ]
                    ),
                    ParentNode(
                        "ul",
                        [
                            ParentNode(
                                "li",
                                [ LeafNode("a", "google", { "href": "google.com" }) ]
                            ),
                            ParentNode(
                                "li",
                                [ LeafNode("a", "netflix", { "href": "netflix.com" }) ]
                            )
                        ]
                    ),
                    ParentNode(
                        "pre",
                        [
                            ParentNode(
                                "code",
                                [ LeafNode(None, "Not sure what to type here.\nSecond line.\n[link](link.com)") ]
                            )
                        ]
                    ),
                    ParentNode(
                        "blockquote",
                        [
                            LeafNode("b", "bolded quote"),
                            LeafNode(None, " with "),
                            LeafNode("code", "inline code")
                        ]
                    ),
                    ParentNode(
                        "h3",
                        [ LeafNode("img", "", { "src": "./img.jpg", "alt": "my image" }), ]
                    ),
                    ParentNode(
                        "p",
                        [ LeafNode(None, "Regular paragraph. Should be on same line.") ]
                    )
                ]
            )
        )
