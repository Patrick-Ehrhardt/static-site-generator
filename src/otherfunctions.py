from textnode import *
import math
import re

def text_to_textnodes(text):
    if isinstance(text, str):
        text = TextNode(text, TextType.TEXT)
        #print(f"string\ntext = {text}")
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
        #print(f"matches = {matches}")
        #print(f"matches[0] = {matches[0]} \n matches[1] = {matches[1]}")
        remaining_text = node.text
        sections = []
        for i in range (0, len(matches)):
            sections = (remaining_text.split(f"![{matches[i][0]}]({matches[i][1]})", 1))
            if sections[0] and sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            if matches[i][0] and matches[i][1]:
                new_nodes.append(TextNode(matches[i][0], TextType.IMAGE, matches[i][1]))
            if len(sections) > 1:
                remaining_text = sections[1]
        if len(remaining_text) > 0:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
            
        #print(f"sections: {sections}")
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    if not isinstance(old_nodes, list):
        old_nodes = [old_nodes]
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            #print(f"node.text_type = {node.text_type}, passing")
            continue
        matches = extract_markdown_links(node.text)
        if not matches:
            new_nodes.append(node)
            continue
        #print(f"matches = {matches}")
        #print(f"matches[0] = {matches[0]} \n matches[1] = {matches[1]}")
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
            
        #print(f"sections: {sections}")
    #print(f"input nodes: {old_nodes}")
    #print(f"output nodes: {new_nodes}")
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

"""
def split_nodes_delimiter(old_nodes, delimiter, text_type): 
    #print("Running function")
    if not delimiter:
        raise Exception(ValueError("No delimiter"))
    new_nodes = []
    if not isinstance(old_nodes, list):
        old_nodes_list = []
        old_nodes_list.append(old_nodes)
    else:
        old_nodes_list = old_nodes
    for node in old_nodes_list:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_text = list(node.text)
        split_indices = []
        no_match = True
        #print(split_text)
        #print(f"delimiter: {delimiter}")
        for i in range (0, len(split_text)):
            if split_text[i] == delimiter:
                #if len(delimiter) == 2 and split_text[i-1] == delimiter:
                    #split_indices.append(i-1)
                #elif len(delimiter) == 2 and split_text[i+1] == delimiter:
                    #split_indices.append(i+1)
                split_indices.append(i)
                no_match = False
        #print(f"split_indices = {split_indices}")
        if no_match:
            new_nodes.append(node)
            print(f"no match {delimiter}")
            continue
        if len(split_indices) %2 == 1:
            raise Exception("Invalid syntax: missing closing delimiter")
        
        if split_indices[0] > 0:
            new_nodes.append(TextNode("".join(split_text[:split_indices[0]]), TextType.TEXT))
        #print(f"len(split_indices): {len(split_indices)}")

        for i in range (0, len(split_indices)):
            #print(f"i: {i}\ntext: {split_text[split_indices[i]]}")
            if split_text[split_indices[i]] == delimiter and i%2 == 0:
                print(f"len(delimiter) = {len(delimiter)}\ndelimiter: {delimiter}")
                new_nodes.append(TextNode("".join(split_text[split_indices[i] + 1:split_indices[i+1]]), text_type))
            elif i + 1 >= len(split_indices):
                if(len(split_text[split_indices[i] + 1:]) > 0): #Dont add next element if its empty
                    new_nodes.append(TextNode("".join(split_text[split_indices[i] + 1:]), TextType.TEXT))
            else:
                new_nodes.append(TextNode("".join(split_text[split_indices[i] + 1:split_indices[i+1]]), TextType.TEXT))
            #print(new_nodes)
    return new_nodes

"""

""" Originally wrote function for single old_node, converted to list. 
def split_nodes_delimiter(old_nodes, delimiter, text_type): 
    #print("Running function")
    if not delimiter:
        raise Exception(ValueError("No delimiter"))
    split_text = list(old_nodes.text)
    split_indices = []
    #print(split_text)
    #print(f"delimiter: {delimiter}")
    for i in range (0, len(split_text)):
        if split_text[i] == delimiter:
            split_indices.append(i)
    #print(f"split_indices = {split_indices}")
    if len(split_indices) %2 == 1:
        raise Exception("Invalid syntax: missing closing delimiter")
    new_nodes = []
    if split_indices[0] > 0:
        new_nodes.append(TextNode("".join(split_text[:split_indices[0]]), TextType.TEXT))
    #print(f"len(split_indices): {len(split_indices)}")
    for i in range (0, len(split_indices)):
        #print(f"i: {i}\ntext: {split_text[split_indices[i]]}")
        if split_text[split_indices[i]] == delimiter and i%2 == 0:
            new_nodes.append(TextNode("".join(split_text[split_indices[i] + 1:split_indices[i+1]]), text_type))
        elif i + 1 >= len(split_indices):
            new_nodes.append(TextNode("".join(split_text[split_indices[i] + 1:]), TextType.TEXT))
        else:
            new_nodes.append(TextNode("".join(split_text[split_indices[i] + 1:split_indices[i+1]]), TextType.TEXT))
        #print(new_nodes)
    return new_nodes
"""

"""
for i in range (0, math.ceil(len(split_indices)/2) + 1, 2):
        print("appending in for loop")
        new_nodes.append(TextNode("".join(split_text[split_indices[i] +1 : split_indices[i+1]]), text_type))
        if i+2 < len(split_indices):
            new_nodes.append(TextNode("".join(split_text[split_indices[i+1] +1 : split_indices[i+2]]), TextType.TEXT))
        else:
            new_nodes.append(TextNode("".join(split_text[split_indices[i+1] +1 :]), TextType.TEXT))
"""