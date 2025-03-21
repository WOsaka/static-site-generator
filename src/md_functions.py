from textnode import TextNode, TextType
from re import findall

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
