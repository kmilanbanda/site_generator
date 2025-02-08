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
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.NORMAL:
            image = extract_markdown_images(node.text)
            if image == None or len(image) == 0:
                new_nodes.append(node)
            else:
                split_str = node.text.split(f"![{image[0][0]}]({image[0][1]})", 1)
                for i in range(0, len(split_str)):
                        if i == 0:
                            if split_str[i] != "":
                                new_nodes.append(TextNode(split_str[i], TextType.NORMAL))
                        if i == 1:
                            new_nodes.append(TextNode(image[0][0], TextType.IMAGE, image[0][1]))
                            if split_str[i] != "":
                                new_nodes.append(TextNode(split_str[i], TextType.NORMAL))                          
        else:
            new_nodes.append(node)
    return new_nodes
    

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.NORMAL:
            link = extract_markdown_links(node.text)
            if link == None or len(link) == 0:
                new_nodes.append(node)
            else:
                split_str = node.text.split(f"[{link[0][0]}]({link[0][1]})", 1)
                for i in range(0, len(split_str)):
                        if i == 0:
                            if split_str[i] != "":
                                new_nodes.append(TextNode(split_str[i], TextType.NORMAL))
                        if i == 1:
                            new_nodes.append(TextNode(link[0][0], TextType.LINK, link[0][1]))
                            if split_str[i] != "":
                                new_nodes.append(TextNode(split_str[i], TextType.NORMAL))                          
        else:
            new_nodes.append(node)
    return new_nodes