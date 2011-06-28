'''
Created on Jan 3, 2011

@author: xiwang
'''
import os
import wx
import sys
import application
from utils.utils import copyfile
from main_dialog import MainDialog
from utils.utils import executeCommand

class App(wx.App):
    DEFAULT_CONFIG_XML = 'config.xml'
    DEFAULT_COMPUTERS_XML = 'computers.xml'
    
    def __init__(self):
        wx.App.__init__(self)
        wx.InitAllImageHandlers()
        self.__initApp()
        self._main_dialog = MainDialog()
        self.SetTopWindow(self._main_dialog)
        
    def __initApp(self):
        src_path = ''
        
        #TODO: adds other platform support here
        if sys.platform == 'linux2':
            src_path = '/etc/remote-desktop'
        
        if not os.path.exists(src_path):
            # only support to copied code for using
            src_path = '%s%sconfig' % (os.path.dirname(__file__), os.path.sep) 
        
        usr_home_path = os.environ['HOME']
        
        ''' check user config home folder '''
        config_home_path = '%s%s%s' % (usr_home_path, os.path.sep, '.RemoteDesktop')
        if not os.path.exists(config_home_path):
            os.makedirs(config_home_path)
        
        ''' check config xml '''
        config_file_template_path = '%s%s%s' % (src_path, os.path.sep, App.DEFAULT_CONFIG_XML)
        config_file_path = '%s%s%s' % (config_home_path, os.path.sep, 'config.xml')
        
        if not os.path.exists(config_file_path) and os.path.exists(config_file_template_path):
            copyfile(config_file_template_path, config_file_path)
            
        ''' check computers xml '''
        computers_file_template_path = '%s%s%s' % (src_path, os.path.sep, App.DEFAULT_COMPUTERS_XML)
        computers_file_path = '%s%s%s' % (config_home_path, os.path.sep, 'computers.xml')
        
        if not os.path.exists(computers_file_path) and os.path.exists(computers_file_template_path):
            copyfile(computers_file_template_path, computers_file_path)
            
        ''' load configuration files '''
        application.CONFIG_FILE_PATH = config_file_path
        application.COMPUTERS_FILE_PATH = computers_file_path
        application.loadConfig()
        
    def start(self):
        loop = True
        while loop:
            ret_code = self._main_dialog.ShowModal()
            if ret_code == wx.ID_OK:
                self.connect()
            else:
                loop = False
                
        self._main_dialog.Destroy()
        self.MainLoop()
        
    def connect(self):
        computer = self._main_dialog.cbx_computer.GetValue().strip()
        if computer == '':
            return
        
        username = self._main_dialog.cbx_username.GetValue().strip()
        if username == '':
            return
        
        domain = ''
        try:
            if username.index('\\'):
                domain, username = username.split('\\')
        except ValueError as ex:
            if ex[0] == 'too many values to unpack': # there is too many '\' in username
                return #TODO: show message dialog to indicates the username is invalid.
            # exception will be ignored if ex[0] == 'substring not found'. it means there is no '\' in username
            else:
                try:
                    if username.index('/'):
                        domain, username = username.split('/')
                except ValueError as ex:
                    if ex[0] == 'too many values to unpack': # there is too many '/' in username
                        return #TODO: show message dialog to indicates the username is invalid.
                    # exception will be ignored if ex[0] == 'substring not found'. it means there is no '/' in username
        
        password = self._main_dialog.txt_password.GetValue().strip()
        if password == '':
            return
        
        resolution = self._main_dialog.cbx_resolution.GetValue().strip()
        if resolution == '':
            return
        
        cmd = 'rdesktop -z'
        
        if self._main_dialog.cb_use_seamless_mode.IsChecked():
            cmd += ' -D -K -a 16'
            
        if self._main_dialog.cb_enable_theme.IsChecked():
            cmd += ' -x l'
            
        if resolution != u'Full Screen':
            cmd += ' -g "%s"' % resolution
        else:
            cmd += ' -f'
        if domain != u'':
            cmd += ' -d "%s"' % domain
        if username != u'':
            cmd += ' -u "%s"' % username
        if password != u'':
            cmd += ' -p "%s"' % password
        if computer != u'':
            cmd += ' "%s"' % computer
        
        succeed, outs, errs = executeCommand(cmd)
        if succeed:
            dirty = False
            if application.Computers.has_key(computer):
                cp = application.Computers[computer]
                if cp.getUsers().has_key(username):
                    user = cp.getUsers()[username]
                    if user.getDomain() != domain:
                        new_user = application.User(domain, username)
                        cp.getUsers()[username] = new_user
                        dirty = True
                else:
                    new_user = application.User(domain, username)
                    cp.getUsers()[username] = new_user
                    dirty = True
                if resolution != '' and cp.getResolution() != resolution:
                    cp.setResolution(resolution)
                    dirty = True
            else:
                cp = application.Computer(computer, resolution)
                new_user = application.User(domain, username)
                cp.getUsers()[username] = new_user
                application.Computers[computer] = cp
                dirty = True
                
            if dirty:
                application.saveConfig() 

if __name__ == '__main__':
    app = App()
    app.start()
