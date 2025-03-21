from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("tag is required")
        if not self.children:
            raise ValueError("children are required")
        html_str = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html_str += child.to_html()
        html_str += f"</{self.tag}>"
        return html_str

    def __repr__(self):
        return f"ParentNode({self.tag if self.tag else 'tag: None'}, {self.children if self.children else 'children: None'}, {self.props if self.props else 'props: None'})"
