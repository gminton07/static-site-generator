import unittest
from textnode import TextNode, TextType
from md_delimiter import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_text_node

class TestMDSplitDelimiter(unittest.TestCase):
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

    def test_split_bold_start(self):
        node = TextNode(
            "**Starting the** sentence as bold.",
            TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertListEqual(
            [
                TextNode("Starting the", TextType.BOLD),
                TextNode(" sentence as bold.", TextType.TEXT),
            ],
            new_nodes,
        )
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
        self.assertListEqual(
            [
                TextNode("italic", TextType.ITALIC)
            ],
            new_nodes
        )
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


class TestMDExtractImageLink(unittest.TestCase):
    def test_extract_image(self):
        md = "![Cat Photo](/cat/png), ![More cat pics](/cat/image/png.jpeg)"
        expected = [("Cat Photo", "/cat/png"), ("More cat pics", "/cat/image/png.jpeg")]
        match = extract_markdown_images(md)
        self.assertEqual(len(match), 2)
        self.assertListEqual(match, expected)
        pass

    def test_extract_link(self):
        md = "Here  is the hyperlink [for github](https://www.github.com). And open [this](localhost://8888:90) for your server."
        match = extract_markdown_links(md)
        expected = [("for github", "https://www.github.com"), ("this", "localhost://8888:90")]
        self.assertEqual(len(match), 2)
        self.assertListEqual(match, expected)
        pass

    def test_extract_link_bad(self):
        md = "![Puppy](/Images/puppy.bmp)"
        match = extract_markdown_links(md)
        expected = []
        self.assertListEqual(match, expected)
        pass

    def test_extract_image_bad(self):
        md = "[YouTube](https://www.youtube.com)"
        match = extract_markdown_images(md)
        expected = []
        self.assertListEqual(match, expected)
        pass


class TestMDSplitImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
        pass

    def test_split_image_after(self):
        node = TextNode(
            "This text has an ![image](https://i.imgur.com/)embedded in it",
            TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This text has an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/"),
                TextNode("embedded in it", TextType.TEXT),
            ],
            new_nodes,
        )
        pass

    def test_split_image_nb4(self):
        node = TextNode(
            "![This image](C://User/Pictures/frame.png) has a picture frame",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This image", TextType.IMAGE, "C://User/Pictures/frame.png"),
                TextNode(" has a picture frame", TextType.TEXT),
            ],
            new_nodes,
        )
        pass

    def test_split_image_only(self):
        node = TextNode(
            "![Image Only](Image/URL)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Image Only", TextType.IMAGE, "Image/URL")
            ],
            new_nodes
        )
        pass


class TestMDSplitLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
        pass

    def test_split_link_after(self):
        node = TextNode(
            "This text has an [link](https://i.imgur.com/)embedded in it",
            TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This text has an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/"),
                TextNode("embedded in it", TextType.TEXT),
            ],
            new_nodes,
        )
        pass

    def test_split_link_nb4(self):
        node = TextNode(
            "[This link](C://User/Pictures/frame.png) has a picture frame",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This link", TextType.LINK, "C://User/Pictures/frame.png"),
                TextNode(" has a picture frame", TextType.TEXT),
            ],
            new_nodes,
        )
        pass

    def test_split_link_only(self):
        node = TextNode(
            "[Link Only](Link/URL)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Link Only", TextType.LINK, "Link/URL")
            ],
            new_nodes
        )
        pass

class TestTexttoTextNode(unittest.TestCase):
    def test_split_to_text_node(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_text_node(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )
        pass

    '''
    def test_split_italic_in_bold(self):
        md = "Nested **bold _italic_ text** test"
        new_nodes = text_to_textnode(md)
        # Will fail for now:
        self.assertListEqual(
            [
                TextNode("Nested ", TextType.TEXT),
                TextNode("bold ", TextType.BOLD),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.BOLD),
                TextNode(" test", TextType.TEXT),
            ],
            new_nodes,
        )
        pass
    '''
