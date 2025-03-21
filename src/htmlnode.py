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
        return f"HTMLNode({self.tag if self.tag else "tag: None"}, {self.value if self.value else "value: None"}, {self.children if self.children else "children: None"}, {self.props if self.props else "props: None"})"
