# -*- coding: utf-8 -*-
import wx # type: ignore
from pubsub import pub # type: ignore
from typing import Optional

class Account(wx.Panel):
    def __init__(self, parent: wx.TreeCtrl, name: Optional[str] = None):
        super(Account, self).__init__(parent=parent)
        self.name = name
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.login = wx.Button(self, wx.ID_ANY, _("Login")) # type: ignore
        self.login.Bind(wx.EVT_BUTTON, lambda event: pub.sendMessage("account.login", name=name))
        sizer.Add(self.login, 0, wx.ALL, 5)
        self.autologin = wx.CheckBox(self, wx.ID_ANY, _("Log in automatically")) # type: ignore
        self.autologin.Bind(wx.EVT_CHECKBOX, lambda event: pub.sendMessage("account.autologin", name=self.name, autologin=self.autologin.GetValue()))
        sizer.Add(self.autologin, 0, wx.ALL, 5)
        self.SetSizer(sizer)

class EmptyBuffer(wx.Panel):
    def __init__(self, parent: wx.TreeCtrl, name: Optional[str] = None):
        super(EmptyBuffer, self).__init__(parent=parent, name=name)
        self.name = name
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
