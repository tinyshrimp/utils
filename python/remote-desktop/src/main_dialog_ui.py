#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Mon May 30 16:51:58 2011

import wx

# begin wxGlade: extracode
# end wxGlade



class RemoteDesktopDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: RemoteDesktopDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE|wx.MINIMIZE_BOX|wx.DIALOG_NO_PARENT|wx.FULL_REPAINT_ON_RESIZE
        wx.Dialog.__init__(self, *args, **kwds)
        self.lbl_computer = wx.StaticText(self, -1, "Computer", style=wx.ALIGN_CENTRE)
        self.cbx_computer = wx.ComboBox(self, -1, choices=[], style=wx.CB_DROPDOWN|wx.CB_SIMPLE|wx.CB_DROPDOWN|wx.CB_SORT)
        self.lbl_user = wx.StaticText(self, -1, "User Name", style=wx.ALIGN_CENTRE)
        self.cbx_username = wx.ComboBox(self, -1, choices=[], style=wx.CB_DROPDOWN|wx.CB_SIMPLE|wx.CB_DROPDOWN|wx.CB_SORT)
        self.lbl_password = wx.StaticText(self, -1, "Password", style=wx.ALIGN_CENTRE)
        self.txt_password = wx.TextCtrl(self, -1, "", style=wx.TE_PASSWORD)
        self.lbl_resolution = wx.StaticText(self, -1, "Resolution")
        self.cbx_resolution = wx.ComboBox(self, -1, choices=[], style=wx.CB_DROPDOWN|wx.CB_SIMPLE|wx.CB_DROPDOWN)
        self.cb_enable_theme = wx.CheckBox(self, -1, "Enable Theme")
        self.cb_use_seamless_mode = wx.CheckBox(self, -1, "Use Seamless Mode")
        self.btn_connect = wx.Button(self, -1, "Connect")
        self.btn_cancel = wx.Button(self, -1, "Quit")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_TEXT, self.on_enter_computer_name, self.cbx_computer)
        self.Bind(wx.EVT_COMBOBOX, self.on_computer_selection_changed, self.cbx_computer)
        self.Bind(wx.EVT_TEXT, self.on_enter_user_name, self.cbx_username)
        self.Bind(wx.EVT_COMBOBOX, self.on_user_selection_changed, self.cbx_username)
        self.Bind(wx.EVT_BUTTON, self.on_connect, self.btn_connect)
        self.Bind(wx.EVT_BUTTON, self.on_quit, self.btn_cancel)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: RemoteDesktopDialog.__set_properties
        self.SetTitle("Remote Desktop")
        self.cbx_computer.SetMinSize((200, 29))
        self.cbx_username.SetMinSize((200, 29))
        self.txt_password.SetMinSize((200, 27))
        self.cbx_resolution.SetMinSize((200, 29))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: RemoteDesktopDialog.__do_layout
        grid_sizer_3 = wx.FlexGridSizer(5, 3, 0, 0)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_4 = wx.FlexGridSizer(7, 3, 0, 0)
        grid_sizer_3.Add((20, 20), 0, 0, 0)
        grid_sizer_3.Add((20, 20), 0, 0, 0)
        grid_sizer_3.Add((20, 20), 0, 0, 0)
        grid_sizer_3.Add((20, 20), 0, 0, 0)
        grid_sizer_4.Add(self.lbl_computer, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_4.Add((10, 20), 0, 0, 0)
        grid_sizer_4.Add(self.cbx_computer, 0, 0, 0)
        grid_sizer_4.Add((20, 8), 0, 0, 0)
        grid_sizer_4.Add((10, 8), 0, 0, 0)
        grid_sizer_4.Add((20, 8), 0, 0, 0)
        grid_sizer_4.Add(self.lbl_user, 0, wx.EXPAND, 0)
        grid_sizer_4.Add((10, 20), 0, 0, 0)
        grid_sizer_4.Add(self.cbx_username, 0, 0, 0)
        grid_sizer_4.Add((20, 8), 0, 0, 0)
        grid_sizer_4.Add((10, 8), 0, 0, 0)
        grid_sizer_4.Add((20, 8), 0, 0, 0)
        grid_sizer_4.Add(self.lbl_password, 0, wx.EXPAND, 0)
        grid_sizer_4.Add((10, 20), 0, 0, 0)
        grid_sizer_4.Add(self.txt_password, 0, 0, 0)
        grid_sizer_4.Add((20, 8), 0, 0, 0)
        grid_sizer_4.Add((10, 8), 0, 0, 0)
        grid_sizer_4.Add((20, 8), 0, 0, 0)
        grid_sizer_4.Add(self.lbl_resolution, 0, wx.EXPAND, 0)
        grid_sizer_4.Add((10, 20), 0, 0, 0)
        grid_sizer_4.Add(self.cbx_resolution, 0, 0, 0)
        grid_sizer_3.Add(grid_sizer_4, 1, wx.EXPAND, 0)
        grid_sizer_3.Add((20, 20), 0, 0, 0)
        grid_sizer_3.Add((20, 20), 0, 0, 0)
        sizer_1.Add(self.cb_enable_theme, 0, 0, 0)
        sizer_1.Add(self.cb_use_seamless_mode, 0, 0, 0)
        grid_sizer_3.Add(sizer_1, 1, wx.EXPAND, 0)
        grid_sizer_3.Add((20, 20), 0, 0, 0)
        grid_sizer_3.Add((20, 20), 0, 0, 0)
        sizer_2.Add((50, 20), 0, 0, 0)
        sizer_2.Add(self.btn_connect, 0, 0, 0)
        sizer_2.Add((20, 20), 0, 0, 0)
        sizer_2.Add(self.btn_cancel, 0, 0, 0)
        sizer_2.Add((20, 20), 0, 0, 0)
        grid_sizer_3.Add(sizer_2, 1, wx.EXPAND, 0)
        grid_sizer_3.Add((20, 20), 0, 0, 0)
        grid_sizer_3.Add((20, 20), 0, 0, 0)
        grid_sizer_3.Add((20, 20), 0, 0, 0)
        grid_sizer_3.Add((20, 20), 0, 0, 0)
        self.SetSizer(grid_sizer_3)
        grid_sizer_3.Fit(self)
        self.Layout()
        self.Centre()
        # end wxGlade

    def on_enter_computer_name(self, event): # wxGlade: RemoteDesktopDialog.<event_handler>
        print "Event handler `on_enter_computer_name' not implemented!"
        event.Skip()

    def on_computer_selection_changed(self, event): # wxGlade: RemoteDesktopDialog.<event_handler>
        print "Event handler `on_computer_selection_changed' not implemented!"
        event.Skip()

    def on_enter_user_name(self, event): # wxGlade: RemoteDesktopDialog.<event_handler>
        print "Event handler `on_enter_user_name' not implemented!"
        event.Skip()

    def on_user_selection_changed(self, event): # wxGlade: RemoteDesktopDialog.<event_handler>
        print "Event handler `on_user_selection_changed' not implemented!"
        event.Skip()

    def on_connect(self, event): # wxGlade: RemoteDesktopDialog.<event_handler>
        print "Event handler `on_connect' not implemented!"
        event.Skip()

    def on_quit(self, event): # wxGlade: RemoteDesktopDialog.<event_handler>
        print "Event handler `on_quit' not implemented!"
        event.Skip()

# end of class RemoteDesktopDialog


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    remote_desktop_dialog = RemoteDesktopDialog(None, -1, "")
    app.SetTopWindow(remote_desktop_dialog)
    remote_desktop_dialog.Show()
    app.MainLoop()