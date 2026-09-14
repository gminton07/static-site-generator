import unittest
from markdown_to_blocks import markdown_to_blocks, BlockType, block_to_block_type

class TestMarkdownToBlocks(unittest.TestCase):
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
            pass

        def test_markdown_to_blocks_2(self):
            md = """
# This is a title

## Subtitle

Paragraph with **bold**

- list1
- list2
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "# This is a title",
                    "## Subtitle",
                    "Paragraph with **bold**",
                    "- list1\n- list2",
                ]
            )
                    

class TestBlockToBlockType(unittest.TestCase):
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
            block_types = [block_to_block_type(block) for block in blocks]
            self.assertEqual(
                block_types,
                [BlockType.PARAGRAPH, BlockType.PARAGRAPH, BlockType.UNORDERED_LIST],
        )

        def test_markdown_to_blocks_2(self):
            md = """
# This is a title

## Subtitle

Paragraph with **bold**

- list1
- list2

> The Block Quote
> Is stored here

1. Item 1
2. Item 2
3. Item 3
5. Item 5

```
print("Hello world")
```
"""
            blocks = markdown_to_blocks(md)
            block_types = [block_to_block_type(block) for block in blocks]
            self.assertEqual(
                block_types,
                [BlockType.HEADING, BlockType.HEADING, BlockType.PARAGRAPH, BlockType.UNORDERED_LIST, BlockType.QUOTE, BlockType.ORDERED_LIST, BlockType.CODE]
            )
