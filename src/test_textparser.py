import unittest

from textnode import TextNode, TextType
from textparser import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

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

    def test_multiple_markdown_of_same_type(self):
        old_nodes = []
        old_nodes.append(TextNode("**BOLD** and **BRAVE** and **OOGABOOGA**", TextType.NORMAL))
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        test_nodes = [TextNode("BOLD", TextType.BOLD), TextNode(" and ", TextType.NORMAL), TextNode("BRAVE", TextType.BOLD), TextNode(" and ", TextType.NORMAL), TextNode("OOGABOOGA", TextType.BOLD)]

    def test_unmatched_delimiters(self):
        old_nodes = []
        old_nodes.append(TextNode("Ooga *Booga", TextType.NORMAL))
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter(old_nodes, "*",  TextType.ITALIC)

    def test_markdown_image_extraction(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        lst1 = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(lst1, extract_markdown_images(text))

    def test_markdown_link_extraction(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        lst1 = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(lst1, extract_markdown_links(text))

    def test_image_markdown(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        lst1 = [TextNode("This is text with a ", TextType.NORMAL), TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif")]
        self.assertEqual(lst1, split_nodes_image([TextNode(text, TextType.NORMAL)]))

    def test_link_markdown(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        lst1 = [TextNode("This is text with a link ", TextType.NORMAL), TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")]
        self.assertEqual(lst1, split_nodes_link([TextNode(text, TextType.NORMAL)]))

    def test_multi_image_markdown(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        lst1 = [TextNode("This is text with a ", TextType.NORMAL), TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"), TextNode(" and ", TextType.NORMAL), TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(lst1, split_nodes_image([TextNode(text, TextType.NORMAL)]))

    def test_multi_link_markdown(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        lst1 = [TextNode("This is text with a link ", TextType.NORMAL), TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"), TextNode(" and ", TextType.NORMAL), TextNode("to youtube", TextType.LINK,  "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(lst1, split_nodes_link([TextNode(text, TextType.NORMAL)]))

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        lst1 = [
                TextNode("This is ", TextType.NORMAL),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.NORMAL),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://boot.dev")
            ]
        self.assertEqual(text_to_textnodes(text), lst1)
        