'''
Created on Jan 4, 2011

@author: xiwang
'''

from utils.xmlLoader import *
from utils.xmlWriter import *

CONFIG_FILE_PATH = ''
Resolutions = []

COMPUTERS_FILE_PATH = ''
Computers = {}
    
def loadConfig():
    ''' load config.xml '''
    if not os.path.exists(CONFIG_FILE_PATH):
        return
    
    config_loader = XmlLoader()
    config_root = config_loader.load(CONFIG_FILE_PATH)
    
    for subNode in config_root.getChildren():
        if subNode.getName().lower() == 'resolutions':
            for resolutionNode in subNode.getChildren():
                Resolutions.append(resolutionNode.getCharData())
                
    ''' load computers.xml '''
    if not os.path.exists(COMPUTERS_FILE_PATH):
        return
    
    computers_loader = XmlLoader()
    computers_root = computers_loader.load(COMPUTERS_FILE_PATH)
    for computerNode in computers_root.getChildren():
        uri = computerNode.getAttrs()['uri']
        resolution = computerNode.getAttrs()['resolution']
        computer = Computer(uri, resolution)
        for userNode in computerNode.getChildren():
            domain = userNode.getAttrs()['domain']
            name = userNode.getAttrs()['name']
            computer.getUsers()[name] = User(domain, name)
        Computers[uri] = computer
                                

def saveConfig():
    if COMPUTERS_FILE_PATH == '':
        return
    
    # adds computers
    computersNode = XmlNode()
    computersNode.setName('computers')
    
    for item in Computers.values():
        computer = XmlNode()
        computer.setName('computer')
        computer.getAttrs()['uri'] = item.getUri()
        computer.getAttrs()['resolution'] = item.getResolution()
        
        # adds users
        for subItem in item.getUsers().values():
            user = XmlNode()
            user.setName('user')
            user.getAttrs()['domain'] = subItem.getDomain()
            user.getAttrs()['name'] = subItem.getName()
            computer.getChildren().append(user)
            
        computersNode.getChildren().append(computer)
    
    xml_writer = XmlWriter(COMPUTERS_FILE_PATH)
    xml_writer.write(computersNode)

def getLogger():
    return None


class Computer(object):
    def __init__(self, uri, resolution):
        self._uri = uri
        self._resolution = resolution
        self._users = {}
        
    def getUri(self):
        return self._uri
    
    def getResolution(self):
        return self._resolution
    
    def setResolution(self, resolution):
        self._resolution = resolution
    
    def getUsers(self):
        return self._users
    
class User(object):
    def __init__(self, domain, name):
        self._domain = domain
        self._name = name
        
    def getDomain(self):
        return self._domain
    
    def getName(self):
        return self._name
