from enum import Enum
from htmlnode import HTMLNode
from textnode import TextNode, text_node_to_html_node
from leafnode import LeafNode
from parentnode import ParentNode
from textparser import text_to_textnodes

import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "orderedlist"

def markdown_to_blocks(markdown):
    blocks = []
    split_text = markdown.split("\n\n")
    for text in split_text:
        if text !=  "":
            text = text.strip()
            blocks.append(text)
    return blocks

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("* ") or block.startswith("- "):
        for line in lines:
            if not line.startswith("* ") and not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

# This function encompasses the entire transformation from markdown to html nodes
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    child_nodes = []
    for block in blocks:
        child_nodes.append(block_to_html_node(block))
    return ParentNode("div", None, child_nodes)

def block_to_html_node(block):
    match block_to_block_type(block):
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block)
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)


# takes a string (text) and returns a list of HTMLNodes (TextNode -> HTMLNode). 
def text_to_children(text):
    children_nodes = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        children_nodes.append(text_node_to_html_node(node))
    return children_nodes

def block_text_to_inline_nodes(block):
    inline_nodes = []
    lines = block.split("\n")
    for line in lines:
        inline_nodes.append(text_to_children(line))
    return inline_nodes

def heading_to_html_node(block):
    count = 0
    for char in block[0:7]:
        if char == "#":
            count += 1
        else:
            break
    if count + 1 >= len(block):
        raise ValueError(f"invalid heading level: {count}")
    text = block[count + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{count}", None, children)

def code_to_html_node(block):
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", None, children)
    return ParentNode("pre", None, [code])

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        new_lines.append(line.lstrip(">").strip())
    text = " ".join(new_lines)
    children =  text_to_children(text)
    return ParentNode("blockquote", None, children)

def unordered_list_to_html_node(block):
    lines = block.split("\n")
    items = []
    for line in lines:
        text = line[2:]
        children = text_to_children(text)
        items.append(ParentNode("li", None, children))
    return ParentNode("ul", None, items)

def ordered_list_to_html_node(block):
    lines = block.split("\n")
    items = []
    for line in lines:
        text = line[3:]
        children = text_to_children(text)
        items.append(ParentNode("li", None, children))
    return ParentNode("ol", None, items)

def paragraph_to_html_node(block):
    lines = block.split("\n")
    text = " ".join(lines)
    children = text_to_children(text)
    return ParentNode("p", None, children)
