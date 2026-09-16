# Imports
import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    #TODO: Allow nested inline elements (bold, italic, etc)
    # Wanted:
    # BOLD <-> ITALIC <-> CODE

    # Current:
    # BOLD -> ITALIC

    new_nodes: list[TextNode] = []

    for node in old_nodes:
        
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue;

        split_nodes: list[TextNode] = []
        split_strings: list[str] = node.text.split(delimiter)
        if len(split_strings) % 2 != 1:
            raise Exception(f'Error: Markdown string has unmatched delimiter: {node.text}')

        for i in range(len(split_strings)):
            if i == 0 and split_strings[0] == '':
                continue;
            elif i % 2 == 1:
                new_text_type = text_type
            else:
                new_text_type = TextType.TEXT

            NODE = TextNode(
                split_strings[i],
                new_text_type
            )
            split_nodes.append(NODE)

        new_nodes.extend(split_nodes)
    
    return new_nodes


def extract_markdown_images(text: str) -> tuple[str, str]:
    # md images: ![alt_text](image_url)
    reg = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(reg, text)
    #print(matches)
    return matches


def extract_markdown_links(text: str) -> tuple[str, str]:
    # md links: [anchor_text](link_url)
    reg = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(reg, text)
    #print(matches)
    return matches


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        # If node is not TEXT type, continue
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue;

        matches = extract_markdown_images(node.text)
        if not matches:     # If matching returns nothing, continue
            new_nodes.append(node)
            continue;
        
        # Split the TextNodes up
        remain_text: str = node.text
        first_loop: bool = True

        for alt, link in matches:
            split_nodes: list[TextNode] = []
            split = remain_text.split(f'![{alt}]({link})', 1)
            
            if first_loop and split[0] == '':
                pass
            else:
                split_nodes.append(
                    TextNode(
                        split[0],
                        TextType.TEXT
                    ),

                )

            split_nodes.append(
                TextNode(
                    alt,
                    TextType.IMAGE,
                    link
                )
            )
            remain_text = split[1]
            first_loop = False

            new_nodes.extend(split_nodes)

        if remain_text != '':
            new_nodes.append(
                TextNode(remain_text, TextType.TEXT)
            )

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue;

        matches = extract_markdown_links(node.text)
        if not matches:
            new_nodes.append(node)
            continue;

        remain_text: str = node.text
        first_loop: bool = True

        for alt, link in matches:
            split_nodes: list[TextNode] = []
            split = remain_text.split(f'[{alt}]({link})', 1)

            if first_loop and split[0] == '':
                pass
            else:
                split_nodes.append(TextNode(
                    split[0],
                    TextType.TEXT,
                ))

            split_nodes.append(
                TextNode(
                    alt,
                    TextType.LINK,
                    link
                )
            )
            remain_text = split[1]
            first_loop = False

            new_nodes.extend(split_nodes)

        if remain_text != '':
            new_nodes.append(
                TextNode(remain_text, TextType.TEXT)
            )
    
    return new_nodes

def text_to_text_node(text: str) -> list[TextNode]:
    first_node = TextNode(text, TextType.TEXT)
    
    bold = split_nodes_delimiter([first_node], "**", TextType.BOLD)
    italic = split_nodes_delimiter(bold, "_", TextType.ITALIC)
    code = split_nodes_delimiter(italic, "`", TextType.CODE)

    images = split_nodes_image(code)
    links = split_nodes_link(images)

    return links
