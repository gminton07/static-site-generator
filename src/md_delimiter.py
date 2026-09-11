# Imports
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    #TODO: Allow nested inline elements (bold, italic, etc)

    new_nodes: list[TextNode] = []

    for node in old_nodes:
        # Only split TextType.TEXT
        # NO nesting

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_nodes: list[TextNode] = []
        split_strings: list[str] = node.text.split(delimiter)
        if len(split_strings) % 2 != 1:
            raise Exception(f'Error: Markdown string has unmatched delimiter: {node.text}')

        for i in range(len(split_strings)):
            if i % 2 == 1:
                new_text_type = text_type
            else:
                new_text_type = TextType.TEXT

            split_nodes.append(
                TextNode(
                    split_strings[i],
                    new_text_type
                )
            )

        new_nodes.extend(split_nodes)
    
    return new_nodes



