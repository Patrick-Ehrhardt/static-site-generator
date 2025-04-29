from textnode import *
from blocks import *
import math
import re
import os

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_file = open(from_path)
    markdown = from_file.read()
    template_file = open(template_path)
    template = template_file.read()
    title = extract_title(markdown)
    print(f"Files opened and read\nlen(markdown) = {len(markdown)}, len(template) = {len(template)}")
    html_node = markdown_to_html_node(markdown)
    print(f"html nodes parsed")
    html = html_node.to_html()
    print(f"html converted len = {len(html)}")
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok = True)
    dest_file = open(dest_path, "w")
    print(f"{dest_file} open")
    dest_file.write(template)
    print(f"dest_file written")
    

def extract_title(markdown):
    split_blocks = markdown_to_blocks(markdown)
    title = None
    for i in range (0, len(split_blocks)):
        if title == None:
            title = re.search("\A#\ .", split_blocks[i]) #This works because our function is splitting into blocks, so it'll be at the beginning of the string. Prevents reading h2-h6 as title
        if isinstance(title, re.Match):
            return split_blocks[i][2:].strip()
    raise Exception("No title found")

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        new_node = block_to_html_node(block)
        nodes.append(new_node)
    parent_node = HTMLNode(tag="div", value = "", children = nodes) #Wrap the entire thing in <div>
    return parent_node

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            content = block.replace("\n", " ")
            new_node = HTMLNode(tag="p", value = "", children = [])
            new_node.children = text_to_children(content) #NYI

        case BlockType.HEADING:
            level = re.search("\A#+ ", block)
            level = level.span()
            print(level)
            level = level[1] - level[0] - 1
            content = block[level:].strip() #Adding two for " "
            new_node = HTMLNode(tag=f"h{level}", value = "", children = [])
            new_node.children = text_to_children(content) #NYI

        case BlockType.CODE:
            block = block.split("```")
            if block[1].startswith("\n"):
                block[1] = block[1][1:]
            new_node = text_node_to_html_node(TextNode(block[1], TextType.TEXT))
            new_node.value = "<pre><code>" + new_node.value + "</code></pre>"

        case BlockType.QUOTE: #Is this supposed to have a paragraph tag inside of blockquote? Mozilla lists one but nothing on boot.dev about it
            #block = block.replace(">", "") #This will strip any ">" inside the quote, also
            content = ""
            split_lines = block.split("\n")
            for line in split_lines:
                content += line[1:] + "\n"
            content = content.rstrip("\n") #Is this ok?
            new_node = HTMLNode(tag="blockquote", value = "", children = [])
            new_node.children = text_to_children(content)

        case BlockType.UNORDERED_LIST:
            content = ""
            split_lines = block.split("\n")
            for line in split_lines:
                content += "<li>" + line[2:] + "</li>" #2 characters stripped for "- "
            content = "".join(content)
            new_node = HTMLNode(tag="ul", value = "", children = [])
            new_node.children = text_to_children(content)

        case BlockType.ORDERED_LIST:
            content = ""
            split_lines = block.split("\n")
            for line in split_lines:
                content += "<li>" + line[3:] + "</li>"
            new_node = HTMLNode(tag= "ol", value = "", children =[])
            new_node.children = text_to_children(content)

        case _:
            raise Exception(ValueError("Invalid BlockType"))

    return new_node

def text_to_children(markdown):
    children = []
    text_nodes = text_to_textnodes(markdown) #We dont need to worry about nested markdown, make a parallel list for the whole block and convert to htmlnode
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    return children



def text_to_textnodes(text):
    if isinstance(text, str):
        text = TextNode(text, TextType.TEXT)
    new_nodes = []
    
    new_nodes = split_nodes_delimiter(text, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes) #images and links scrub empty nodes, split_nodes_delimiter leaves them intact. Reversed order to always scrub empty nodes
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    if not isinstance(old_nodes, list):
        old_nodes = [old_nodes]
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        matches = extract_markdown_images(node.text)
        remaining_text = node.text
        sections = []
        for i in range (0, len(matches)):
            sections = (remaining_text.split(f"![{matches[i][0]}]({matches[i][1]})", 1))
            if sections[0] and sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            if matches[i][0] and matches[i][1]:
                print(f"adding image node\n{TextNode(matches[i][0], TextType.IMAGE, matches[i][1])}")
                new_nodes.append(TextNode(matches[i][0], TextType.IMAGE, matches[i][1]))
            if len(sections) > 1:
                remaining_text = sections[1]
        if len(remaining_text) > 0:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
            
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    if not isinstance(old_nodes, list):
        old_nodes = [old_nodes]
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        matches = extract_markdown_links(node.text)
        if not matches:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        sections = []
        for i in range (0, len(matches)):
            sections = (remaining_text.split(f"[{matches[i][0]}]({matches[i][1]})", 1))
            if sections[0] and sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            if matches[i][0] and matches[i][1]:
                new_nodes.append(TextNode(matches[i][0], TextType.LINK, matches[i][1]))
            #node.text = sections[1]
            if len(sections) > 1:
                remaining_text = sections[1]
        if len(remaining_text) > 0:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
            
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if not delimiter:
        raise Exception(ValueError("No delimiter"))
    if not isinstance(old_nodes, list):
        old_nodes_list = []
        old_nodes_list.append(old_nodes)
    else:
        old_nodes_list = old_nodes
    new_nodes = []
    for node in old_nodes_list:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_text = node.text.split(delimiter)
        for i in range (0, len(split_text)):
            if i % 2 == 0: #even, TextType.TEXT
                new_nodes.append(TextNode(split_text[i], TextType.TEXT))
            if i % 2 == 1: #odd, delimited text
                new_nodes.append(TextNode(split_text[i], text_type))
    return new_nodes

