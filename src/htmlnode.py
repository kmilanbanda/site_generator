

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        if children != None and not isinstance(children, list):
            raise ValueError("All children must be contained in a list")
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        html = ""
        for key, value in self.props:
            html += f" {key}=\"{value}\""
        return html
    
    def __eq__(self, other):
        if (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
            ):
            return True

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
