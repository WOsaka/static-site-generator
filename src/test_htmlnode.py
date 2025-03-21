import unittest
from htmlnode import HTMLNode


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
            "HTMLNode(p, This is a paragraph, children: None, {'class': 'text'})",
        )


if __name__ == "__main__":
    unittest.main()
