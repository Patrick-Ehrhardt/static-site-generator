from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = ""
    HEADING = "#"
    CODE = "```"
    QUOTE = ">"
    UNORDERED_LIST = "-"
    ORDERED_LIST = "."

def block_to_block_type(markdown):
    if len(markdown) < 3:
        return BlockType.PARAGRAPH
    split_text = markdown.split("\n")
    is_quote = True
    is_ordered_list = True
    if re.search("#+\. ", markdown[:8]):
        return BlockType.HEADING
    #if markdown[:3] == "```" and markdown[3:] == "```":
    if re.search("\A```", markdown) and re.search("```\Z", markdown):
        return BlockType.CODE
    if re.search("\A- ", markdown, re.MULTILINE):
        return BlockType.UNORDERED_LIST
    for i in range (0, len(split_text)):
        if split_text[i][0] != ">":
            is_quote = False
        if split_text[i][:3] != str(i + 1) + ". ":
            is_ordered_list = False
    if is_quote:
        return BlockType.QUOTE
    if is_ordered_list:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
    
def markdown_to_blocks(markdown):
    if not isinstance(markdown, str):
        raise Exception("Invalid markdown input, expecting string")
    split_text = markdown.split("\n\n")
    final_text = []
    for line in split_text:
        line = line.strip()
        if line == "":
            continue
        final_text.append(line)
    return final_text