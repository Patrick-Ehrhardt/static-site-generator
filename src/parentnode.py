from htmlnode import *

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)
        if not isinstance(children, list): #Case for single LeafNode being passed instead of a list, convert single element to list
            self.children = []
            self.children.append(children)

    def to_html(self):
        if not self.tag:
            raise Exception(ValueError)
        if not self.children:
            raise Exception(ValueError("Missing value for children"))
        returnStr = f"<{self.tag}>"
        for child in self.children:
            if child: #Protects from None type being passed in list
                returnStr += child.to_html()
        return returnStr + f"</{self.tag}>"
        #return f"<{self.tag}>{self.children.to_html()}</{self.tag}>"