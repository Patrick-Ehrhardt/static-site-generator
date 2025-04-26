
class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = None
        self.value = None
        self.children = None
        self.props = None
        if tag:
            self.tag = tag
        if value:
            self.value = value
        if children:
            self.children = children
        if props:
            self.props = props
        pass

    def to_html(self):
        raise Exception(NotImplementedError)
    
    def props_to_html(self):
        returnStr = ""
        for item in self.props:
            returnStr += " " + item + "=" + '"' + self.props[item] + '"'
        return returnStr
    
    def __repr__(self):
        returnStr = "HTMLNode("
        if self.tag:
            returnStr += self.tag + ", "
        if self.value:
            returnStr += self.value + ", "
        if self.children:
            returnStr += self.children + ", "
        if self.props:
            returnStr += self.props + ", "
        returnStr += ")"
        return returnStr
