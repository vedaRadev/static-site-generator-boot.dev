class HTMLNode:
    # No tag => raw text
    # No value => assumed to have children
    # No children => assumed to have value
    # No props => no attributes
    def __init__(self, tag = None, value = None, children = None, props = None):
        assert value or children

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
