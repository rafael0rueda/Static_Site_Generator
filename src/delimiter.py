from textnode import TextType, TextNode
from htmlnode import HTMLNode,LeafNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if delimiter not in ["`", "*", "**"]:
        raise Exception("Invalid delimiter")
    new_list = []
    for old_node in old_nodes:
        tmp_lst = re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)", old_node.text)
        tmp_lst = [part for part in tmp_lst if part] # remove empty strings from the list
        for e in tmp_lst:
            # change this part code repete multiple times
            if "`" in e:
                if e.count("`") ==2:
                    new_list.append(TextNode(e.replace("`", ""), TextType.CODE))
                else:
                    raise Exception("Invalid Mardown syntax: missing delimiter")
            elif "**" in e:
                if e.count("*") == 4:
                    new_list.append(TextNode(e.replace("**", ""), TextType.BOLD))
                else:
                    raise Exception("Invalid Markdown syntax: missing delimiter")
            elif "*" in e:
                if e.count("*") == 2:
                    new_list.append(TextNode(e.replace("*", ""), TextType.ITALIC))
                else:
                    raise Exception("Invalid Markdown syntax: missing delimiter")
            else:
                new_list.append(TextNode(e, TextType.NORMAL))
        
    return new_list
