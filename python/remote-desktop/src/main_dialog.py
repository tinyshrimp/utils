'''
Created on Jan 3, 2011

@author: xiwang
'''

import wx
import application
from utils.utils import executeCommand
from main_dialog_ui import RemoteDesktopDialog

class MainDialog(RemoteDesktopDialog):
    def __init__(self):
        RemoteDesktopDialog.__init__(self, None, -1, '')
        
        for computerUri in application.Computers.keys():
            self.cbx_computer.Append(computerUri)
            
        for resolution in application.Resolutions:
            self.cbx_resolution.Append(resolution)
            
        if self.cbx_resolution.Count > 0:
            self.cbx_resolution.Select(0)
        
    def on_connect(self, event):
        self.EndModal(wx.ID_OK)
        
    def on_connect(self, event):
        self.EndModal(wx.ID_OK)        

    def on_quit(self, event):
        self.EndModal(wx.ID_CANCEL)
        
    def on_computer_selection_changed(self, event):
        uri = event.String
        if uri != '':        
            computer = application.Computers[uri]
            if computer is None:
                return
            
            resolution = computer.getResolution()
            
            # set resolution
            resolution_index = self.cbx_resolution.FindString(resolution)
            if resolution_index != wx.NOT_FOUND:
                self.cbx_resolution.Select(resolution_index)
            else:
                self.cbx_resolution.SetValue(resolution)
                
            # set users
            self.cbx_username.Clear()
            for user in computer.getUsers().values():
                domain = user.getDomain()
                name = user.getName()
                
                username = name
                if domain != None and domain != '':
                    username = '%s\\%s' % (domain, username)
                    
                self.cbx_username.Append(username)
                
            if self.cbx_username.Count > 0:
                self.cbx_username.Select(0)
        else:
            if self.cbx_resolution.Count > 0:
                self.cbx_resolution.Select(0)
            self.cbx_username.Clear()
            
        ''' clear password '''            
        self.txt_password.SetValue('')
        
    def on_enter_computer_name(self, event):
        if self.txt_password.GetValue().strip() != '':
            self.txt_password.SetValue('')
            
    def on_user_selection_changed(self, event):
        ''' clear password '''
        self.txt_password.SetValue('')
        
    def on_enter_user_name(self, event):
        if self.txt_password.GetValue().strip() != '':
            self.txt_password.SetValue('')

        
