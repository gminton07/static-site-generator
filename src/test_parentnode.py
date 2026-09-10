import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
        pass

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("b", 'Bold text')
        child2 = LeafNode(None, 'Normal text')
        child3 = LeafNode('i', 'italic text')
        parent_node = ParentNode(
            'p',
            [
                child1,
                child2,
                child3,
                child2,
            ],
        )
        expected = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        self.assertEqual(parent_node.to_html(), expected)
        pass

    def test_to_html_no_tag(self):
        child = LeafNode('i', 'italic')
        node = ParentNode(None, [child])
        self.assertRaises(ValueError, node.to_html)
        pass

    def test_to_html_no_child(self):
        node = ParentNode('div', None)
        self.assertRaises(ValueError, node.to_html)
        pass
