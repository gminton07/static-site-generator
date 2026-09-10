import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_init_None(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
        pass

    def test_set_tag(self):
        tag = "h1"
        node = HTMLNode(tag=tag)
        self.assertEqual(tag, node.tag)
        pass

    def test_set_value(self):
        value = "Lorem ipsum dolor sit amet..."
        node = HTMLNode(value=value)
        self.assertEqual(value, node.value)

    def test_props_to_html(self):
        props = {"href": "https://www.google.com",
                 "title" :"Google"}
        html = ' href="https://www.google.com" title="Google"'
        node = HTMLNode(props=props)
        self.assertEqual(props, node.props)
        self.assertEqual(html, node.props_to_html())
