class HTMLNode:
    # No tag => raw text
    # No value => assumed to have children
    # No children => assumed to have value
    # No props => no attributes
    def __init__(self, tag = None, value = None, children = None, props = None):
        # assert value or children

        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


    def to_html(self):
        raise NotImplementedError
    

    # TODO default props to empty dictionary
    def props_to_html(self) -> str:
        result = ""

        if not self.props:
            return result

        for prop in self.props:
            result += f' {prop}="{self.props[prop]}"'

        return result


    def __repr__(self):
        return f"tag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: {self.props}"


    def __eq__(self, other):
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )



class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)


    def to_html(self) -> str:
        # empty string values are ok
        if not self.value and self.value != "":
            raise ValueError("leaf nodes must have values")

        if not self.tag:
            return f"{self.value}"
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)


    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("parent nodes must have tags")
        if not self.children:
            raise ValueError("parent nodes must have children")

        as_html = f"<{self.tag}>"
        for child in self.children:
            as_html += child.to_html()
        as_html += f"</{self.tag}>"
        
        return as_html
