import unittest
from md_functions import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_node,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    text_to_children,
    markdown_to_html_node,
    extract_list_items
)
from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType


class TestFunctions(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_invalid(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_split_nodes_delimiter_empty(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [])

    def test_split_nodes_delimiter_different_type(self):
        node = TextNode("**This is bold**", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [node])

    def test_split_nodes_delimiter_multiple(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_beginning(self):
        node = TextNode("`code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_end(self):
        node = TextNode("This is text with a `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
            ],
        )

    def test_split_nodes_delimiter_different_delimiters(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        text = "This is text with an image ![image](https://www.boot.dev/image.png)"
        self.assertEqual(
            [("image", "https://www.boot.dev/image.png")],
            extract_markdown_images(text),
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            extract_markdown_links(text),
        )

    def test_split_node_image(self):
        node = TextNode(
            "This is text with an image ![image](https://www.boot.dev/image.png)",
            TextType.TEXT,
        )
        new_nodes = split_node(
            node, "image", "https://www.boot.dev/image.png", TextType.IMAGE
        )
        self.assertEqual(
            [
                TextNode("This is text with an image ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://www.boot.dev/image.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_multiple_nodes(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node, node])  # Multiple nodes
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_with_link(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])  # Multiple nodes
        self.assertListEqual(
            [
                TextNode(
                    "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another ",
                    TextType.TEXT,
                ),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_multiple(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node, node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items

    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self):
        self.assertEqual(
            block_to_block_type("This is **bolded** text"), BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("- This is a list\n- with multiple lines"),
            BlockType.UNORDERT_LIST,
        )
        self.assertEqual(
            block_to_block_type("1. This is an ordered list"), BlockType.ORDERED_LIST
        )
        self.assertEqual(
            block_to_block_type("```python\nprint('Hello, World!')\n```"),
            BlockType.CODE,
        )
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        self.assertEqual(
            block_to_block_type("### This is a heading"), BlockType.HEADING
        )

    def test_block_to_block_type_heading(self):
        self.assertEqual(
            block_to_block_type("### This is a heading"), BlockType.HEADING
        )
        self.assertEqual(
            block_to_block_type("###### This is a heading"), BlockType.HEADING
        )
        self.assertEqual(
            block_to_block_type("####### This is a paragraph"), BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("#This is a paragraph"), BlockType.PARAGRAPH
        )

    def test_block_to_block_type_code(self):
        self.assertEqual(
            block_to_block_type("```python\nprint('Hello, World!')\n```"),
            BlockType.CODE,
        )
        self.assertEqual(
            block_to_block_type("```python\nprint('Hello, World!')\n"),
            BlockType.PARAGRAPH,
        )
        self.assertEqual(
            block_to_block_type("python\nprint('Hello, World!')\n```"),
            BlockType.PARAGRAPH,
        )
        self.assertEqual(
            block_to_block_type("-This is a Paragraph"), BlockType.PARAGRAPH
        )

    def test_block_to_block_type_quote(self):
        self.assertEqual(block_to_block_type(">This is a Quote"), BlockType.QUOTE)
        self.assertEqual(
            block_to_block_type(">This is a Quote\n>Quote"), BlockType.QUOTE
        )
        self.assertEqual(
            block_to_block_type(">This is not a Quote\nQuote"), BlockType.PARAGRAPH
        )

    def test_block_to_block_type_unordered_list(self):
        self.assertEqual(
            block_to_block_type("- This is a List"), BlockType.UNORDERT_LIST
        )
        self.assertEqual(
            block_to_block_type("- This is not a List\n-List"), BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("- This is a List\n- List"), BlockType.UNORDERT_LIST
        )

    def test_block_to_block_type_ordered_list(self):
        self.assertEqual(
            block_to_block_type("1. This is a List"), BlockType.ORDERED_LIST
        )
        self.assertEqual(
            block_to_block_type("1. This is a List\n2. List"), BlockType.ORDERED_LIST
        )
        self.assertEqual(
            block_to_block_type("1. This is not a List\n1. List"), BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("1. This is not a List\n2.List"), BlockType.PARAGRAPH
        )

    def test_text_to_children_simple(self):
        text = "This is text with **bolded** text"
        children = text_to_children(text)
        self.assertEqual(
            [
                LeafNode(None, "This is text with ", None),
                LeafNode("b", "bolded", None),
                LeafNode(None, " text", None),
            ],
            children,
        )

    def test_text_to_children(self):
        text = "This is text with **bolded** text and _italic_ text and `code` here"
        children = text_to_children(text)
        self.assertEqual(
            [
                LeafNode(None, "This is text with ", None),
                LeafNode("b", "bolded", None),
                LeafNode(None, " text and ", None),
                LeafNode("i", "italic", None),
                LeafNode(None, " text and ", None),
                LeafNode("code", "code", None),
                LeafNode(None, " here", None),
            ],
            children,
        )

    def test_markdown_to_html_node_heading(self):
        text = "### This is a heading"
        node = markdown_to_html_node(text)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>This is a heading</h3></div>",
        )

    def test_markdown_to_html_node_paragraph(self):
        text = """This is a paragraph with **bolded** text and _italic_ text and `code` here"""
        node = markdown_to_html_node(text)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is a paragraph with <b>bolded</b> text and <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_markdown_to_html_node_code(self):
        text = """
    ```
    python
    print('Hello, World!')
    ```
        """
        node = markdown_to_html_node(text)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>python\nprint('Hello, World!')\n</code></pre></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_markdown_to_html_node_quote(self):
        text = """
    > This is a quote
    > with multiple lines
    > and _italic_ text, **bolded** text, and `code` here
        """
        node = markdown_to_html_node(text)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with multiple lines and <i>italic</i> text, <b>bolded</b> text, and <code>code</code> here</blockquote></div>",
        )

    def test_markdown_to_html_node_unordered_list(self):
        text = """
    - This is a list
    - with items
        """
        node = markdown_to_html_node(text)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li></ul></div>",
        )

    def test_list_items_unordered(self):
        text = "- This is a list\n- with items"
        children = extract_list_items(text)
        self.assertEqual(
            [
                ParentNode("li", [LeafNode(None, "This is a list", None)], None),
                ParentNode("li", [LeafNode(None, "with items", None)], None),
            ],
            children,
        )

    def test_markdown_to_html_node_unordered_list_children(self):
        text = """
    - This is a list with **bolded** text
    - and _italic_ text
        """
        node = markdown_to_html_node(text)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list with <b>bolded</b> text</li><li>and <i>italic</i> text</li></ul></div>",
        )

    def test_markdown_to_html_node_unordered_list_complex(self):
        text = """
    - This is a list with images ![image](https://www.boot.dev/image.png)
    - and links [link](https://www.boot.dev)
        """
        node = markdown_to_html_node(text)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><ul><li>This is a list with images <img src="https://www.boot.dev/image.png" alt="image"></img></li><li>and links <a href="https://www.boot.dev">link</a></li></ul></div>',
        )

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_markdown_to_html_node_ordered_list(self):
        text = """
    1. This is a list
    2. with items
        """
        node = markdown_to_html_node(text)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is a list</li><li>with items</li></ol></div>",
        )