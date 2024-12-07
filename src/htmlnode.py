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
    def props_to_html(self):
        result = ""

        if not self.props:
            return result

        for prop in self.props:
            result += f' {prop}="{self.props[prop]}"'

        return result


    def __repr__(self):
        return f"tag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: {self.props}"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)


    def to_html(self):
        # TODO move this up to the constructor
        if not self.value:
            raise ValueError("leaf nodes must have values")

        if not self.tag:
            return f"{self.value}"
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

