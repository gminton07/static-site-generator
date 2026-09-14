from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = 0
    HEADING = 1
    CODE = 2
    QUOTE = 3
    UNORDERED_LIST = 4
    ORDERED_LIST = 5

def markdown_to_blocks(markdown: str):
    blocks = markdown.split('\n\n')
    return [block.strip() for block in blocks]

def block_to_block_type(block: str) -> BlockType:
    if re.match(r'^#{1,6} ', block):
        return BlockType.HEADING
    elif block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    # Check each line
    block_lines = block.splitlines()
    def startswith(lst: list[str], search: str) -> bool:
        total = (re.match(search, line) for line in lst)
        if None in total:
            return False
        return True

    if startswith(block_lines, r">"):
        return BlockType.QUOTE
    elif startswith(block_lines, r"- "):
        return BlockType.UNORDERED_LIST
    elif startswith(block_lines, r"[\d]+. "):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
