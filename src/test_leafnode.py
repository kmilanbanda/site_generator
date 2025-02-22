import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_neq(self):
        dict1 = {
            "href": "https://www.google.com"
        }
        dict2 = {
            "href": "https://www.boot.dev"
        }
        node = LeafNode("a", "This is the text", None, dict1)
        node2 = LeafNode("a", "This is the text", None, dict2)
        self.assertNotEqual(node, node2)

    def test_validation(self):
        child = LeafNode("p", "This is a child node")
        node = LeafNode("p", "This node has children", [child])
        self.assertIsNone(node.children)

if __name__ == "__main__":
    unittest.main()