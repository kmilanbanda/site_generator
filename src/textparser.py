import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if delimiter == "":
        raise ValueError("Invalid delimiter")

    new_nodes = []
    for node in old_nodes:
        if node.text.count(delimiter) % 2 != 0:
            raise Exception("Unmatched delimiters")
        if node.text_type == TextType.NORMAL:
            split_str = node.text.split(delimiter)
            for i in range(0, len(split_str)):
                if split_str[i] != "":
                    if i % 2 == 1:
                        new_nodes.append(TextNode(split_str[i], text_type))
                    else:
                        new_nodes.append(TextNode(split_str[i], TextType.NORMAL))
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text) #the regex in the tip was !\[([^\[\]]*)\]\(([^\(\)]*)\)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text) # original r"\[(.*?)\]\((.*?)\)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.NORMAL:
            unworked_text = node.text
            images = extract_markdown_images(unworked_text)
            if len(images) == 0:
                new_nodes.append(node)
                continue
            for image in images:
                split_str = unworked_text.split(f"![{image[0]}]({image[1]})", 1)
                if len(split_str) != 2:
                    raise ValueError("Invalid markdown, unclosed image section")
                if split_str[0] != "":
                    new_nodes.append(TextNode(split_str[0], TextType.NORMAL))
                new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                unworked_text = split_str[1]                
            if unworked_text != "":
                new_nodes.append(TextNode(unworked_text, TextType.NORMAL))                     
        else:
            new_nodes.append(node)
    return new_nodes
    

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.NORMAL:
            unworked_text = node.text
            links = extract_markdown_links(unworked_text)
            if  len(links) == 0:
                new_nodes.append(node)
                continue
            for link in links:
                split_str = unworked_text.split(f"[{link[0]}]({link[1]})", 1)
                if len(split_str) != 2:
                    raise ValueError("Invalid markdown, unclosed link section")
                if split_str[0] != "":
                    new_nodes.append(TextNode(split_str[0], TextType.NORMAL))
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                unworked_text = split_str[1]  
            if unworked_text != "":
                new_nodes.append(TextNode(unworked_text, TextType.NORMAL))                                 
        else:
            new_nodes.append(node)
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.NORMAL)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes