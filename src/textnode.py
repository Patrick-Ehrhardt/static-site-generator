from enum import Enum
from leafnode import *
class TextType(Enum):
    TEXT = ""
    BOLD = "**"
    ITALIC = "_"
    CODE = "`"
    LINK = "[]()"
    IMAGE = "~[]()"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other_node):
        if self.text == other_node.text and self.text_type == other_node.text_type:
            if self.url:
                if self.url == other_node.url:
                    return True
            return True
        else:
            return False
        pass

    def __repr__(self):
        return(f"TextNode({self.text}, {self.text_type}, {self.url})")
    

    
def text_node_to_html_node(text_node):
        if not isinstance(text_node, TextNode):
            raise Exception(ValueError("Invalid TextNode type"))
        if text_node.text_type not in TextType:
            raise Exception(ValueError("Invalid text_type, not in TextType enum"))
        match text_node.text_type:
            case TextType.TEXT:
                return LeafNode(None, text_node.text)
            case TextType.BOLD:
                return LeafNode("b", text_node.text)
            case TextType.ITALIC:
                return LeafNode("i", text_node.text)
            case TextType.CODE:
                return LeafNode("code",text_node.text)
            case TextType.LINK:
                return LeafNode("a", text_node.text, {"href"})
            case TextType.IMAGE:
                return LeafNode("img", None, {"src": "alt"}) #Keep an eye on this, not sure how the src and alt text are meant to be passed
            case _:
                raise Exception("Unknown error in text_node_to_html_node")