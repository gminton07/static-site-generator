from enum import Enum
import re
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import text_node_to_html_node, TextNode, TextType
from md_delimiter import text_to_text_node

class BlockType(Enum):
    PARAGRAPH = 0
    HEADING = 1
    CODE = 2
    QUOTE = 3
    UNORDERED_LIST = 4
    ORDERED_LIST = 5

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split('\n\n')
    return [block.strip() for block in blocks]

def block_to_block_type(block: str) -> BlockType:
    if re.match(r'^#{1,6} ', block):
        return BlockType.HEADING
    elif re.match(r"```\n", block) and block.endswith("```"):
        return BlockType.CODE

    # Check each line
    block_lines = block.splitlines()
    def startswith(lst: list[str], search: str) -> bool:
        count = 0
        for line in lst:
            match = re.match(search, line)
            if match is not None:
                count +=1
        if count == len(lst):
            return True
        else:
            return False

    # def startswith(lst: list[str], search: str) -> bool:
    #     count = 0
    #     matches = (re.match(search, line) for line in lst)
    #     for match in matches:
    #         if match is not None:
    #             count += 1
    #     if count == len(lst):
    #         return True
    #     else:
    #         return False

    if startswith(block_lines, r"^(>)"):
        print(f"{block_lines = }, {block = }")
        return BlockType.QUOTE
    elif startswith(block_lines, r"- "):
        return BlockType.UNORDERED_LIST
    elif startswith(block_lines, r"[\d]+. "):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def get_heading_level(block: str) -> int:
    for i in range(6, 0, -1):
        if block.startswith("#" * i):
            return i
    else:
        raise Exception(f"Error: block is not type BlockType.HEADING, {block}")

def block_to_tag(block: str) -> tuple[str, str]:
    block_type = block_to_block_type(block)

    main_tag = ""
    child_tag = ""

    match block_type:
        case BlockType.PARAGRAPH:
            main_tag = "p"
        case BlockType.HEADING:
            level = get_heading_level(block)
            main_tag = f"h{level}"
        case BlockType.CODE:
            main_tag = "pre"
            child_tag = "code"
        case BlockType.QUOTE:
            main_tag = "blockquote"
        case BlockType.UNORDERED_LIST:
            main_tag = "ul"
            child_tag = "li"
        case BlockType.ORDERED_LIST:
            main_tag = "ol"
            child_tag = "li"
            pass
        case _:
            pass

    return main_tag, child_tag

def text_to_children(text: str) -> list[HTMLNode]:
    # Get BlockType
    block_type = block_to_block_type(text)
    main_tag, child_tag = block_to_tag(text)

    def whole_block(text) -> list[HTMLNode]:
        text_nodes = text_to_text_node(text)
        html_nodes = []
        for node in text_nodes:
            html_nodes.append(text_node_to_html_node(node))

        return html_nodes

    def individual_lines(text: str, strip: str, child_tag: str = child_tag) -> list[HTMLNode]:
        lines = text.splitlines()
        html_nodes = []
        for line in lines:
            ## Changed HERE
            line = line.strip()
            line = re.sub(strip, "", line)
            text_nodes = text_to_text_node(line)
            child_nodes = []
            for node in text_nodes:
                child_nodes.append(text_node_to_html_node(node))

            html_nodes.append(ParentNode(child_tag, child_nodes))
        return html_nodes

    # No line splitting
    if block_type == BlockType.PARAGRAPH:
        text = text.replace('\n', ' ')
        html_nodes = whole_block(text)
    elif block_type == BlockType.HEADING:
        level = int(main_tag[1])
        stripped_text = text.lstrip("#" * level + " ")  # #'s for each level
        html_nodes =  whole_block(stripped_text)

    # Line splitting
    elif block_type == BlockType.QUOTE:
        #TODO: SHOULD NOT GET CHILD NODES
        lines = text.splitlines()
        new_lines = []
        for line in lines: 
            new_lines.append(re.sub("^>", "", line))
        new_text = "\n".join(new_lines)
        text_nodes = text_to_text_node(new_text)
        child_nodes = []
        for node in text_nodes:
            child_nodes.append(text_node_to_html_node(node))
        return ParentNode(main_tag, child_nodes)


    elif block_type == BlockType.UNORDERED_LIST:
        html_nodes = individual_lines(text, r"- ")
    elif block_type == BlockType.ORDERED_LIST:
        html_nodes = individual_lines(text, r"[\d]+. ")

    parent_node = ParentNode(main_tag, html_nodes)
    return parent_node

    

    # if CODE: WTF
    # if multilined: split lines apart
    # For each line:
        # Strip MD stuff away ('#', '- ', '1. ', '>', etc) Based on BlockType
        # text_to_text_node(line)
        # text_node_to_html_node(text_node)
        # Accumulate html_nodes
        # if child_tag: ParentNode(child_tag, html_nodes)
        # Accumulate ParentNodes
    # return list[ParentNode]
    pass

def markdown_to_html_node(markdown: str) -> HTMLNode:
    # Split markdown in to blocks
    blocks = markdown_to_blocks(markdown)
    parent_nodes: list[HTMLNode] = []

    for block in blocks:
        # Check that block has data
        if block == "":
            continue;
        
        # Get BlockType
        block_type = block_to_block_type(block)

        if block_type == BlockType.CODE:   # Code block
            text = block.lstrip("```\n").rstrip("```")
            text_node = TextNode(text, TextType.CODE)
            node = text_node_to_html_node(text_node)
            parent = ParentNode("pre", [node])
            parent_nodes.append(parent)
            continue

        # Create new HTMLNode with proper data
        node = text_to_children(block)
        parent_nodes.append(node)

    # Combine all parent_nodes into a ParentNode
    return ParentNode("div", parent_nodes) 