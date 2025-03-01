from enum import Enum
from textnode import TextType, TextNode, text_node_to_html_node
from htmlnode import HTMLNode,LeafNode, ParentNode
from markdown_oneline import text_to_textnodes
import re

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [bl.strip() for bl in blocks]
    return blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block_markdown):
    if  "# " in block_markdown:
            if re.findall(r"^#{1,}", block_markdown)[0].count("#") > 6:
                 raise Exception("Invalid number of #")
            return BlockType.HEADING
    elif "```" in block_markdown:
         if re.findall(r"\`{3}[\s\S]*?\`{3}", block_markdown):
            return BlockType.CODE
         raise Exception("Invalid syntax for code block")
    elif  "> " in block_markdown:
            quotes = block_markdown.split("\n")
            quotes = [part for part in quotes if part]
            for quote in quotes:
                 if re.findall(r"^>", quote):
                      continue
                 else:
                      raise Exception("Invalid syntax for qoute")          
            return BlockType.QUOTE
    elif  "- " in block_markdown:
            lst = block_markdown.split("\n")
            lst = [part for part in lst if part]
            for l in lst:
                 if re.findall(r"^- ", l):
                      continue
                 else:
                      raise Exception("Invalid syntax for unordred list")          
            return BlockType.UNORDERED_LIST
    elif "1." in block_markdown:
         lst = block_markdown.split("\n")
         lst = [part for part in lst if part]
         for l in lst:
              if re.findall(r"^\d.", l):
                   continue
              else:
                   raise Exception("Invalid sysntax for order list")
         return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
         node = block_to_html_node(block)
         children.append(node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

# test = """
# This is **bolded** paragraph
# text in a p
# tag here

# This is another paragraph with _italic_ text and `code` here

# """
# markdown_to_html_node(test)