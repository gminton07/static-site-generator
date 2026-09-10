import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        pass

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
        pass

    def test_repr_eq(self):
        text = "Cute cat pictures"
        text_type = TextType.IMAGE
        url = "./cat.png"
        expected = f'TextNode({text}, {text_type.value}, {url})'
        node = TextNode(text, text_type, url)
        self.assertEqual(expected, str(node))
        


if __name__ == '__main__':
    unittest.main()
