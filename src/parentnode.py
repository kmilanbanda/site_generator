from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, value, children=None, props=None):
        super().__init__(tag, "", children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode must have a tag.")
        if self.children == None:
            raise ValueError("ParentNode must have children")
        href = ""
        if self.props != None:
            href = self.props_to_html()
        children_text = ""
        for child in self.children:
            children_text = children_text + child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_text}</{self.tag}>"
