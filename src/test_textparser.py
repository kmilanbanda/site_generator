import unittest

from textnode import TextNode, TextType
from textparser import split_nodes_delimiter

class TestTextParser(unittest.TestCase):
    def test_bold_markdown(self):
        old_nodes = []
        old_nodes.append(TextNode("This is what **BOLD** text looks like.", TextType.NORMAL))
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        test_nodes = [TextNode("This is what ", TextType.NORMAL), TextNode("BOLD", TextType.BOLD), TextNode(" text looks like.", TextType.NORMAL)]
        self.assertEqual(test_nodes, new_nodes)

    def test_italic_markdown(self):
        old_nodes = []
        old_nodes.append(TextNode("This is what *italic* text looks like.", TextType.NORMAL))
        new_nodes = split_nodes_delimiter(old_nodes, "*", TextType.ITALIC)
        test_nodes = [TextNode("This is what ", TextType.NORMAL), TextNode("italic", TextType.ITALIC), TextNode(" text looks like.", TextType.NORMAL)]
        self.assertEqual(test_nodes, new_nodes)

    def test_multiple_markdown(self):
        old_nodes = []
        old_nodes.append(TextNode("Now try **BOLD** and *italic* text.", TextType.NORMAL))
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        new_nodes = (split_nodes_delimiter(new_nodes, "*", TextType.ITALIC))
        test_nodes = [TextNode("Now try ", TextType.NORMAL), TextNode("BOLD", TextType.BOLD), TextNode(" and ", TextType.NORMAL), TextNode("italic", TextType.ITALIC), TextNode(" text.", TextType.NORMAL)]
        self.assertEqual(test_nodes, new_nodes)

    def test_markdown_on_right_edge(self):
        old_nodes = []
        old_nodes.append(TextNode("Get a load of **THIS**", TextType.NORMAL))
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        test_nodes = [TextNode("Get a load of ", TextType.NORMAL), TextNode("THIS", TextType.BOLD)]
        self.assertEqual(test_nodes, new_nodes)
    
    def test_markdown_on_left_edge(self):
        old_nodes = []
        old_nodes.append(TextNode("*Get* a load of THIS", TextType.NORMAL))
        new_nodes = split_nodes_delimiter(old_nodes, "*", TextType.ITALIC)
        test_nodes = [TextNode("Get", TextType.ITALIC), TextNode(" a load of THIS", TextType.NORMAL)]
        self.assertEqual(test_nodes, new_nodes)

    def test_markdown_on_whole_text(self):
        old_nodes = []
        old_nodes.append(TextNode("**FEEL THE HEAT**", TextType.NORMAL))
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        test_nodes = [TextNode("FEEL THE HEAT", TextType.BOLD)]
        self.assertEqual(test_nodes, new_nodes)

    def test_unmatched_delimiters(self):
        old_nodes = []
        old_nodes.append(TextNode("Ooga *Booga", TextType.NORMAL))
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter(old_nodes, "*",  TextType.ITALIC)