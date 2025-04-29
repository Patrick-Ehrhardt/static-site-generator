from htmlnode import *

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            return ""
            raise Exception(ValueError)
        if self.tag == None:
            return self.value
        #if self.tag == "img" and self.props:
            #return f'<img src="{self.props_to_html()}>{self.value}</img>'
        if self.props:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        