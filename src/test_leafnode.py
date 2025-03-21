import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
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
