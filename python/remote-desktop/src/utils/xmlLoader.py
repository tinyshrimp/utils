'''
Created on Jun 5, 2010

@author: tinyshrimp
'''

import os

from xml.parsers.expat import ParserCreate

class XmlNode(object):
    def __init__(self):
        self._name = ''
        self._attrs = None
        self._charData = ''
        self._children = None
        
    def getName(self):
        return self._name
    
    def setName(self, name):
        self._name = name
    
    def getCharData(self):
        return self._charData
    
    def setCharData(self, charData):
        self._charData = charData
        
    def getAttrs(self):
        if self._attrs is None:
            self._attrs = {}
        return self._attrs
    
    def getChildren(self):
        if self._children is None:
            self._children = []
        return self._children
    
    def dump(self):
        print self.str()
        for child in self.getChildren():
            child.dump()
    
    def str(self):
        attrs = ''
        for attr in self.getAttrs():
            if '' != attrs:
                attrs += ','
            attrs += "%s:%s" % (attr, self.getAttrs()[attr])
        return "name:%s attrs:{%s} charData:%s" % (self.getName(), attrs, self.getCharData())
        

class XmlLoader(object):
    def __init__(self):
        self._parser = None   
        
    def load(self, filename):
        if None is filename or '' == filename or not os.path.exists(filename):
            return None
        
        self._curNode = None
        self._stack = []
        self._root = None
        
        file = open(filename, 'r')
        self.__getParser().ParseFile(file)
        
        return self._root
        
    def __getParser(self):
        if self._parser is None:
            self._parser = ParserCreate()
            self._parser.StartElementHandler = self.__start_element
            self._parser.EndElementHandler = self.__end_element
            self._parser.CharacterDataHandler = self.__char_data
        return self._parser
    
    def __start_element(self, name, attrs):
        node = XmlNode()
        node.setName(name.lower())
        for attr in attrs:
            node.getAttrs()[attr.lower()] = attrs[attr]
            
        if self._root is None:
            self._root = node
            self._curNode = node
        else:
            self._stack.append(self._curNode)
            self._curNode.getChildren().append(node)
            self._curNode = node
    
    def __end_element(self, name):
        if 0 < len(self._stack):
            self._curNode = self._stack.pop()
    
    def __char_data(self, data):
        data = data.strip()
        if '' != data and self._curNode is not None:
            self._curNode.setCharData(data)
            