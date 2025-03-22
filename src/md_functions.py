from textnode import TextNode, TextType
from re import findall, search
from enum import Enum


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        sub_nodes = text.split(delimiter)
        if len(sub_nodes) % 2 != 1:
            raise ValueError("invalid Markdown syntax")

        sub_nodes_to_textnode = []
        for i in range(len(sub_nodes)):
            if i % 2 == 0:
                type = TextType.TEXT
            else:
                type = text_type

            if len(sub_nodes[i]) == 0:
                continue

            new_node = TextNode(sub_nodes[i], type)
            sub_nodes_to_textnode.append(new_node)
        new_nodes.extend(sub_nodes_to_textnode)

    return new_nodes


def extract_markdown_images(text):
    matches = findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_node(node, alt, link, text_type):
    if text_type not in [TextType.IMAGE, TextType.LINK]:
        raise ValueError("invalid text type")

    pattern = f"![{alt}]({link})" if text_type == TextType.IMAGE else f"[{alt}]({link})"
    nodes_to_textnode = []
    text = node.text
    sub_nodes = text.split(pattern)
    for i in range(len(sub_nodes)):
        if sub_nodes[i] != "":
            nodes_to_textnode.append(TextNode(sub_nodes[i], TextType.TEXT))
        if i < len(sub_nodes) - 1:
            nodes_to_textnode.append(TextNode(alt, text_type, link))

    return nodes_to_textnode


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue

        split_on_img = [node]
        for alt, link in images:
            split_on_img = [
                sub_node
                for node in split_on_img
                for sub_node in (
                    split_node(node, alt, link, TextType.IMAGE)
                    if node.text_type == TextType.TEXT
                    and alt in node.text
                    and link in node.text
                    else [node]
                )
            ]

        new_nodes.extend(split_on_img)

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue

        split_on_link = [node]
        for alt, url in links:
            split_on_link = [
                sub_node
                for node in split_on_link
                for sub_node in (
                    split_node(node, alt, url, TextType.LINK)
                    if node.text_type == TextType.TEXT
                    and alt in node.text
                    and url in node.text
                    else [node]
                )
            ]

        new_nodes.extend(split_on_link)

    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    split_b = split_nodes_delimiter([node], "**", TextType.BOLD)
    split_b_i = split_nodes_delimiter(split_b, "_", TextType.ITALIC)
    split_b_i_c = split_nodes_delimiter(split_b_i, "`", TextType.CODE)
    split_b_i_c_img = split_nodes_image(split_b_i_c)
    split_b_i_c_img_lnk = split_nodes_link(split_b_i_c_img)
    return split_b_i_c_img_lnk


def markdown_to_blocks(markdown):
    block_strings = markdown.split("\n\n")

    cleaned_blocks = []
    for block in block_strings:
        lines = block.split("\n")
        cleaned_block = "\n".join(line.strip() for line in lines if line != "")
        cleaned_blocks.append(cleaned_block.strip())

    return cleaned_blocks


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERT_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(text):
    if search(r"^(#{1,6})\s(.+)", text):
        return BlockType.HEADING
    elif text[:3] == "```" and text[-3:] == "```":
        return BlockType.CODE
    elif text[0] == ">":
        for line in text.split("\n"):
            if line[0] != ">":
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif text[:2] == "- ":
        for line in text.split("\n"):
            if line[:2] != "- ":
                return BlockType.PARAGRAPH
        return BlockType.UNORDERT_LIST
    elif text[:3] == "1. ":
        lines = text.split("\n")
        for i in range(len(lines)):
            start = f"{i + 1}. "
            if lines[i][: len(start)] != start:
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
