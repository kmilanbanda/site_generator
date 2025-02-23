import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("a", "This is the text")
        node2 = HTMLNode("a", "This is the text")
        self.assertEqual(node, node2)

    def test_neq(self):
        dict1 = {
            "href": "https://www.google.com"
        }
        dict2 = {
            "href": "https://www.boot.dev"
        }
        node = HTMLNode("a", "This is the text", None, dict1)
        node2 = HTMLNode("a", "This is the text", None, dict2)
        self.assertNotEqual(node, node2)

    def test_neq_children(self):
        dict1 = {
            "href": "https://www.google.com"
        }
        node = HTMLNode("a", "This is the text", None, dict1)
        node2 = HTMLNode("a", "This is the text", None, dict1)
        lst = [node, node2]
        node3 = HTMLNode("a", "This is the text", lst, dict1)
        self.assertNotEqual(node, node3)
    
    def test_props_to_html(self):
        dict1 = {
            "href": "https://www.google.com"
        }
        
        node = HTMLNode("a", "This is the text", None, dict1)
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\"")

if __name__ == "__main__":
    unittest.main()
