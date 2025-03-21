from textnode import TextNode, TextType

def main():
    text_node = TextNode("Some text", TextType.LINK, "www.google.de")
    print(text_node)

if __name__ == "__main__":
    main()