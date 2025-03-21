from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("value is required")
        if not self.tag:
            return self.value
        html_str = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return html_str

    def __repr__(self):
        return f"LeafNode({self.tag if self.tag else 'tag: None'}, {self.value if self.value else 'value: None'}, {self.props if self.props else 'props: None'})"
