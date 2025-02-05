import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_link(self):
        node = TextNode("This is a text node", TextType.BOLD, "www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "www.boot.dev")
        self.assertEqual(node, node2)

    def test_neq_link(self):
        node = TextNode("This is a text node", TextType.BOLD, "www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_neq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_conversion_normal(self):
        node = TextNode("text", TextType.NORMAL)
        self.assertEqual(text_node_to_html_node(node), LeafNode(None, "text"))

    def test_conversion_bold(self):
        node = TextNode("bold", TextType.BOLD)
        self.assertEqual(text_node_to_html_node(node).to_html(), LeafNode("b", "bold").to_html())

    def test_conversion_italic(self):
        node = TextNode("italic", TextType.ITALIC)
        self.assertEqual(text_node_to_html_node(node), LeafNode("i", "italic"))

    def test_conversion_code(self):
        node = TextNode("code", TextType.CODE)
        self.assertEqual(text_node_to_html_node(node), LeafNode("code", "code"))

    def test_conversion_link(self):
        node = TextNode("link", TextType.LINK, "www.google.com")
        self.assertEqual(text_node_to_html_node(node), LeafNode("a", "link", None, {"href": "www.google.com"}))

    def test_conversion_image(self):
        node = TextNode("alt", TextType.IMAGE, "www.imagesrc.com")
        dct1 = {
            "src": "www.imagesrc.com",
            "alt": "alt"
        }
        self.assertEqual(text_node_to_html_node(node), LeafNode("img", None, None, dct1))

if __name__ == "__main__":
    unittest.main()
