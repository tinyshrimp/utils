'''
Created on Jul 14, 2010

@author: tinyshrimp
'''

class XmlWriter(object):
    def __init__(self, filename):
        self._filename = filename
    
    def write(self, rootNode):
        self._file = open(self._filename, 'w')
        self._file.write('<?xml version="1.0" encoding="utf-8"?>\n')
        self._file.write('\n')
        self.__writeElement(rootNode, 0)
        self._file.close()
    
    def __writeElement(self, xmlNode, indent):
        if 0 != len(xmlNode.getChildren()):
            self.__writeElementWithChildren(xmlNode.getName(), xmlNode.getAttrs(), xmlNode.getChildren(), indent)
        elif '' != xmlNode.getCharData():
            self.__writeElementWithCharData(xmlNode.getName(), xmlNode.getAttrs(), xmlNode.getCharData(), indent)
        else:
            self.__writeSingleElement(xmlNode.getName(), xmlNode.getAttrs(), indent)
        
    def __writeElementWithChildren(self, name, attrs, childNodes, indent):
        if name is None or '' == name:
            return
        
        attrStr = self.__getAttrsString(attrs)
        if attrStr is None or '' == attrStr:
            elementStart = '%s<%s>\n' % ('\t' * indent, name)
        else:
            elementStart = '%s<%s %s>\n' % ('\t' * indent, name, attrStr)
            
        elementEnd = '%s</%s>\n' % ('\t' * indent, name)
        
        self._file.write(elementStart)
        if childNodes is not None and 0 < len(childNodes):
            for childNode in childNodes:
                self.__writeElement(childNode, indent + 1)
        self._file.write(elementEnd)
        
    def __writeElementWithCharData(self, name, attrs, charData, indent):
        if name is None or '' == name:
            return
        
        print 'Name: %s, Attrs: %s, CharData: %s' % (name, attrs, charData)
        
        attrStr = self.__getAttrsString(attrs)
        if attrStr is None or '' == attrStr:
            elementStart = '%s<%s>\n' % ('\t' * indent, name)
        else:
            elementStart = '%s<%s %s>\n' % ('\t' * indent, name, attrStr)
            
        elementEnd = '%s</%s>\n' % ('\t' * indent, name)
        
        self._file.write(elementStart)
        self._file.write('\t' * (indent + 1) + charData + '\n')
        self._file.write(elementEnd)
        
    def __writeSingleElement(self, name, attrs, indent):
        attrStr = self.__getAttrsString(attrs)
        if attrStr is None or '' == attrStr:
            element = '%s<%s/>\n' % ('\t' * indent, name)
        else:
            element = '%s<%s %s/>\n' % ('\t' * indent, name, attrStr)
        self._file.write(element)        
        
    def __getAttrsString(self, attrs):
        if attrs is None or 0 == len(attrs.keys()):
            return None
        
        attrStr = ''
        for key in attrs.keys():
            value = attrs.get(key)
            attrStr += '%s=\'%s\' ' % (key, value)
        return attrStr.strip()
            