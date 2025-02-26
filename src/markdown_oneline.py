from textnode import TextType, TextNode
from htmlnode import HTMLNode,LeafNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if delimiter not in ["`", "*", "**"]:
        raise Exception("Invalid delimiter")
    new_list = []
    for old_node in old_nodes:
        if old_node.text_type == TextType.IMAGES or old_node. text_type == TextType.LINKS:
            new_list.append(old_node)
            continue
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

def extract_markdown_images(text):
    images_alt = re.findall(r"!\[(.*?)\]", text)
    images_alt = [ alt.replace("!", "") for alt in images_alt ]
    images_url = re.findall(r"\((.*?)\)", text)   
    images_list = []
    for i in range(len(images_alt)):
        images_list.append((images_alt[i], images_url[i]))
    return images_list


def extract_markdown_links(text):
    link_anchor = re.findall(r"(?<!!)\[(.*?)\]", text)
    link_url = re.findall(r"\((.*?)\)", text)   
    link_list = []
    for i in range(len(link_anchor)):
        link_list.append((link_anchor[i], link_url[i]))
    return link_list

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        copy_text = node.text
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image in images:
            sections = copy_text.split(f"![{image[0]}]({image[1]})",1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))
            new_nodes.append(TextNode(image[0], TextType.IMAGES, image[1]))
            copy_text = sections[1]
            #print(copy_text)
        if copy_text != "":
             new_nodes.append(TextNode(copy_text, TextType.NORMAL))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        copy_text = node.text
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for link in links:
            sections = copy_text.split(f"[{link[0]}]({link[1]})",1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))
            new_nodes.append(TextNode(link[0], TextType.LINKS, link[1]))
            copy_text = sections[1]
        if copy_text != "":
            new_nodes.append(TextNode(copy_text, TextType.NORMAL))

    return new_nodes

def text_to_textnodes(text):
    text_node = TextNode(text, TextType.NORMAL) 
    text_node = split_nodes_image([text_node])
    text_node = split_nodes_link(text_node)
    text_node = split_nodes_delimiter(text_node, "*", TextType.NORMAL)
    
    return text_node

#test = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
#text_to_textnodes(test)