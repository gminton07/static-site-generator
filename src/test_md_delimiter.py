import unittest
from textnode import TextNode, TextType
from md_delimiter import split_nodes_delimiter

class TestMDDelimiter(unittest.TestCase):
    def test_split_bold(self):
        md = "This is text with a **bolded phrase** in the middle"
        node = TextNode(
            md,
            TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        
        # Check TextTypes
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

        # Check substrings
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[1].text, "bolded phrase")
        self.assertEqual(new_nodes[2].text, " in the middle")
        pass


    def test_split_double_bold(self):
        md = "This line **has** two **bold** segments"
        node = TextNode(
            md,
            TextType.TEXT
        )
        new_nodes = split_nodes_delimiter(
                [node],
                '**',
                TextType.BOLD
        )
        self.assertEqual(len(new_nodes), 5)

        # Check TextTypes
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)

        # Check substrings
        self.assertEqual(new_nodes[0].text, "This line ")
        self.assertEqual(new_nodes[1].text, "has")
        self.assertEqual(new_nodes[2].text, " two ")
        self.assertEqual(new_nodes[3].text, "bold")
        self.assertEqual(new_nodes[4].text, " segments")
        pass

    def test_split_italic(self):
        md = "This _word_ is in italics"
        node = TextNode(md, TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '_', TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)

        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        pass

    def test_split_italic_only(self):
        md = "italic"
        node = TextNode(md, TextType.ITALIC)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)
        pass

    def test_split_code(self):
        md = """
        In python: `print("hello world")`
        In C:
        `#include <stdio.h>
        void main() {
            printf("Hello world");
            return;
        }`
        """
        node = TextNode(md, TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 5)

        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[1].text, 'print("hello world")')
        pass

    def test_bold_code_italic(self):
        md = "This sentence has **bold**, _italic_, and `code` elements."
        node = TextNode(md, TextType.TEXT)
        
        bold_split = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(bold_split[0].text_type, TextType.TEXT)
        self.assertEqual(bold_split[1].text_type, TextType.BOLD)
        self.assertEqual(bold_split[2].text_type, TextType.TEXT)

        italic_split = split_nodes_delimiter(bold_split, "_", TextType.ITALIC)
        self.assertEqual(italic_split[3].text_type, TextType.ITALIC)
        self.assertEqual(italic_split[4].text_type, TextType.TEXT)

        code_split = split_nodes_delimiter(italic_split, "`", TextType.CODE)

        self.assertEqual(code_split[5].text_type, TextType.CODE)
        self.assertEqual(code_split[6].text_type, TextType.TEXT)
        pass

    #def test_split_nested(self):
    #    md = "Nested **bold _italic_ text** test"
    #    node = TextNode(md, TextType.TEXT)
    #    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    #    # Will fail for now:
    #    self.assertEqual(len(new_nodes), 5)
    #    pass

