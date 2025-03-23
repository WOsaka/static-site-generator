class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        str = ""
        if self.props:
            for key, value in self.props.items():
                str += f' {key}="{value}"'
        return str

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, value):
        return (
            self.tag == value.tag
            and self.value == value.value
            and self.children == value.children
            and self.props == value.props
        )

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError(f"value is required for {self}")
        if self.tag is None:
            return self.value
        html_str = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return html_str

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag is required")
        if self.children is None:
            raise ValueError("children are required")
        html_str = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html_str += child.to_html()
        html_str += f"</{self.tag}>"
        return html_str

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
