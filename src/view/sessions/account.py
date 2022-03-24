# -*- coding: utf-8 -*-
import wx

class Account(wx.Panel):
    def __init__(self, parent, name=None):
        super(Account, self).__init__(parent=parent)
        self.name = name
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.login = wx.Button(self, wx.ID_ANY, _("Login"))
        sizer.Add(self.login, 0, wx.ALL, 5)
        self.autostart = wx.CheckBox(self, wx.ID_ANY, _("Log in automatically"))
        sizer.Add(self.autostart, 0, wx.ALL, 5)
        self.SetSizer(sizer)

class EmptyBuffer(wx.Panel):
    def __init__(self, parent, name=None):
        super(EmptyBuffer, self).__init__(parent=parent, name=name)
        self.name = name
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
