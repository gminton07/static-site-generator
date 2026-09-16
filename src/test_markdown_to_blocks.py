import unittest
from markdown_to_blocks import markdown_to_blocks, BlockType, block_to_block_type, markdown_to_html_node

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

###No space

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
                [BlockType.HEADING, BlockType.HEADING, BlockType.PARAGRAPH, BlockType.PARAGRAPH, BlockType.UNORDERED_LIST, BlockType.QUOTE, BlockType.ORDERED_LIST, BlockType.CODE]
            )


class TestMarkdownToHTMLNode(unittest.TestCase):
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

    def test_heading_levels(self):
        md = """
# Heading level 1

## Heading level 2

### Heading level 3

#### Heading level 4

##### Heading level 5

###### Heading level 6
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
             html,
             "<div><h1>Heading level 1</h1><h2>Heading level 2</h2><h3>Heading level 3</h3><h4>Heading level 4</h4><h5>Heading level 5</h5><h6>Heading level 6</h6></div>"
        )
        pass

    def test_ordered_list(self):
        md = """
1. First Item
2. Second item
3. Third item"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
             html,
             "<div><ol><li>First Item</li><li>Second item</li><li>Third item</li></ol></div>"
        )
        pass

    def test_unordered_list(self):
        md = """
# Grocery List

- Lettuce
- Bread
- Milk
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
             html, 
             "<div><h1>Grocery List</h1><ul><li>Lettuce</li><li>Bread</li><li>Milk</li></ul></div>"
        )
        pass

    def test_block_quote(self):
        md = """
## Block Quotation

>Believe you can and you're halfway there.
>
> Theodore Roosevelt

Should not get block quote 1 > 2 = False
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
                html, 
                "<div><h2>Block Quotation</h2><blockquote>Believe you can and you're halfway there.\n\n Theodore Roosevelt</blockquote><p>Should not get block quote 1 > 2 = False</p></div>"
        )
        pass

