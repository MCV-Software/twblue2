# -*- coding: utf-8 -*-
import wx
from pubsub import pub

class Account(wx.Panel):
    def __init__(self, parent, name=None):
        super(Account, self).__init__(parent=parent)
        self.name = name
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.login = wx.Button(self, wx.ID_ANY, _("Login"))
        self.login.Bind(wx.EVT_BUTTON, lambda event: pub.sendMessage("account.login", name=name))
        sizer.Add(self.login, 0, wx.ALL, 5)
        self.autologin = wx.CheckBox(self, wx.ID_ANY, _("Log in automatically"))
        self.autologin.Bind(wx.EVT_CHECKBOX, lambda event: pub.sendMessage("account.autologin", name=self.name, autologin=self.autologin.GetValue()))
        sizer.Add(self.autologin, 0, wx.ALL, 5)
        self.SetSizer(sizer)

class EmptyBuffer(wx.Panel):
    def __init__(self, parent, name=None):
        super(EmptyBuffer, self).__init__(parent=parent, name=name)
        self.name = name
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
