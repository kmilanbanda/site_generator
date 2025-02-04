import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_child(self):
        converted_text = "<p><b>Bold Text</b></p>"
        node = LeafNode("b", "Bold Text")
        lst = [node]
        parent = ParentNode("p", "", lst)
        self.assertEqual(converted_text, parent.to_html())
        

    def test_children(self):
        converted_text = "<p><b>Bold Text</b>Normal text<i>italic text</i>Normal text</p>"
        node = LeafNode("b", "Bold Text")
        node2 = LeafNode(None, "Normal text")
        node3 = LeafNode("i", "italic text")
        node4 = LeafNode(None, "Normal text")
        children = [node, node2, node3, node4]

        parent = ParentNode("p", "", children)
        self.assertEqual(converted_text, parent.to_html())

    def test_no_child(self):
        parent = ParentNode("p", "")
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_nested_parents(self):
        converted_text = "<p><i>italic text</i><b>Bold Text</b></p>"
        node = LeafNode("b", "Bold Text")
        node2 = LeafNode("i", "italic text")
        
        children1 = [node]
        parent1 = ParentNode("p", "", children1)
        children2 = [node2, parent1]
        parent2 = ParentNode("p", "", children2)
        self.assertNotEqual(converted_text, parent2.to_html())

if __name__ == "__main__":
    unittest.main()