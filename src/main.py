import os
import shutil
from re import findall
from textnode import TextNode, TextType
from md_functions import markdown_to_html_node


def main():
    move_directory("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")


def move_directory(source, destination):
    # Ensure the destination directory is clean
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.makedirs(destination)

    for entry in os.listdir(source):
        source_path = os.path.join(source, entry)
        destination_path = os.path.join(destination, entry)
        if os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)
        elif os.path.isdir(source_path):
            move_directory(source_path, destination_path)


def extract_titel(markdown):
    first_line = markdown.strip().split("\n")[0]
    heading = findall(r"^(#{1})\s(.+)", first_line)
    if len(heading) != 0:
        return heading[0][1].strip()
    raise Exception("no h1 header")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        markdown = file.read()
    with open(template_path) as file:
        template = file.read()
    content = markdown_to_html_node(markdown).to_html()
    title = extract_titel(markdown)
    structured_html = template.replace("{{ Title }}", title)
    structured_html = structured_html.replace("{{ Content }}", content)

    dest_dir, _ = os.path.split(dest_path)
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    with open(dest_path, "w") as file:
        file.write(structured_html)


if __name__ == "__main__":
    main()
