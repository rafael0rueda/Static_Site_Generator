from enum import Enum
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