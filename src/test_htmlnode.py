import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Welcome to the site!",
            None,
            {"class": "welcome", "href": "https://example.com"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="welcome" href="https://example.com"',
        )

    def test_to_html_props_empty(self):
        node = HTMLNode("div", "Welcome to the site!", None, {})
        self.assertEqual(node.props_to_html(), "")

    def test_to_html_props_none(self):
        node = HTMLNode("div", "Welcome to the site!", None, None)
        self.assertEqual(node.props_to_html(), "")

    def test_to_html_props_multiple(self):
        node = HTMLNode(
            "div",
            "Welcome to the site!",
            None,
            {"class": "welcome", "id": "header", "style": "font-size: 20px;"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="welcome" id="header" style="font-size: 20px;"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "Enjoy your stay",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "Enjoy your stay",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "This is a paragraph",
            None,
            {"class": "text"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, This is a paragraph, None, {'class': 'text'})",
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()  # This should raise a ValueError

    def test_leaf_to_html_props(self):
        node = LeafNode(
            "a",
            "Click me!",
            {"href": "https://example.com"},
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://example.com">Click me!</a>',
        )

    def test_leaf_to_html_props_empty(self):
        node = LeafNode("a", "Click me!", {})
        self.assertEqual(node.to_html(), "<a>Click me!</a>")

    def test_leaf_to_html_props_none(self):
        node = LeafNode("a", "Click me!", None)
        self.assertEqual(node.to_html(), "<a>Click me!</a>")

    def test_leaf_to_html_props_multiple(self):
        node = LeafNode(
            "a",
            "Click me!",
            {"class": "button", "id": "clickme", "style": "font-size: 20px;"},
        )
        self.assertEqual(
            node.to_html(),
            '<a class="button" id="clickme" style="font-size: 20px;">Click me!</a>',
        )

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "parent"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="parent"><span>child</span></div>',
        )

    def test_to_html_no_tag(self):
        parent_node = ParentNode(None, [])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_multiple_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("span", "child2")
        child_node3 = LeafNode(None, "child3")
        parent_node = ParentNode("div", [child_node1, child_node2, child_node3])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child1</span><span>child2</span>child3</div>",
        )

    def test_to_html_with_multiple_children_and_multiple_grandchildren(self):
        grandchild_node1 = LeafNode("b", "grandchild1")
        grandchild_node2 = LeafNode("b", "grandchild2")
        child_node1 = ParentNode("span", [grandchild_node1, grandchild_node2])
        child_node2 = LeafNode("span", "child2")
        child_node3 = LeafNode(None, "child3")
        parent_node = ParentNode("div", [child_node1, child_node2, child_node3])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild1</b><b>grandchild2</b></span><span>child2</span>child3</div>",
        )


if __name__ == "__main__":
    unittest.main()
