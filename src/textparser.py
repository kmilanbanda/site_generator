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

