# -*- coding: utf-8 -*-
""" Base GUI class for the Session manager module."""
import wx # type: ignore
from pubsub import pub # type: ignore
from typing import List

class SessionManagerWindow(wx.Dialog):
    """ Dialog that displays all session managing capabilities to users. """
    def __init__(self):
        super(SessionManagerWindow, self).__init__(parent=None, title=_(u"Session manager"), size=wx.DefaultSize)
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(panel, -1, _(u"Accounts list"), size=wx.DefaultSize)
        listSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.list = wx.ListBox(panel, wx.ID_ANY)
        listSizer.Add(label, 0, wx.ALL, 5)
        listSizer.Add(self.list, 0, wx.ALL, 5)
        sizer.Add(listSizer, 0, wx.ALL, 5)
        self.new = wx.Button(panel, wx.ID_ANY, _("New account"), size=wx.DefaultSize)
        self.new.Bind(wx.EVT_BUTTON, self.on_new_account)
        self.remove = wx.Button(panel, wx.ID_ANY, _("Remove account"))
        self.remove.Bind(wx.EVT_BUTTON, self.on_remove)
        self.configuration = wx.Button(panel, wx.ID_ANY, _("Global Settings"))
        self.configuration.Bind(wx.EVT_BUTTON, self.on_configuration)
        ok = wx.Button(panel, wx.ID_OK, size=wx.DefaultSize)
        ok.SetDefault()
        cancel = wx.Button(panel, wx.ID_CANCEL, size=wx.DefaultSize)
        buttons = wx.BoxSizer(wx.HORIZONTAL)
        buttons.Add(self.new, 0, wx.ALL, 5)
        buttons.Add(self.configuration, 0, wx.ALL, 5)
        buttons.Add(ok, 0, wx.ALL, 5)
        buttons.Add(cancel, 0, wx.ALL, 5)
        sizer.Add(buttons, 0, wx.ALL, 5)
        panel.SetSizer(sizer)
        min = sizer.CalcMin()
        self.SetClientSize(min)

    def fill_list(self, sessionsList: List[str]):
        for i in sessionsList:
            self.list.Append(i)
        if self.list.GetCount() > 0:
            self.list.SetSelection(0)

    def ok(self, ev: wx.Event):
        if self.list.GetCount() == 0:
            wx.MessageDialog(self, _("You need to configure an account."), _("Account Error"), wx.ICON_ERROR).ShowModal() # type: ignore
            return
        self.EndModal(wx.ID_OK)

    def on_new_account(self, *args, **kwargs):
        menu = wx.Menu()
        rss = menu.Append(wx.ID_ANY, _("Rss feed"))
        twitter = menu.Append(wx.ID_ANY, _("Twitter"))
        mastodon = menu.Append(wx.ID_ANY, _("Mastodon"))
        menu.Bind(wx.EVT_MENU, lambda event: pub.sendMessage("sessionmanager.new_account", type="rss"), rss)
        menu.Bind(wx.EVT_MENU, lambda event: pub.sendMessage("sessionmanager.new_account", type="twitter"), twitter)
        menu.Bind(wx.EVT_MENU, lambda event: pub.sendMessage("sessionmanager.new_account", type="mastodon"), mastodon)
        self.PopupMenu(menu, self.new.GetPosition())

    def add_new_session_to_list(self):
        total = self.list.GetCount()
        name = _("Authorized account %d") % (total+1)
        self.list.Append(name)
        if self.list.GetCount() == 1:
            self.list.SetSelection(0)

    def on_remove(self, *args, **kwargs):
        dlg = wx.MessageDialog(self, _("Do you really want to delete this account?"), _("Remove account"), wx.YES_NO)
        response = dlg.ShowModal()
        dlg.Destroy()
        if response == wx.ID_YES:
            selected = self.list.GetSelection()
            pub.sendMessage("SessionManager.remove_account", index=selected)

    def on_configuration(self, *args, **kwargs):
        pub.sendMessage("sessionmanager.configuration")

    def remove_session(self, sessionID: str):
        self.list.remove_item(sessionID)

    def hide_configuration(self):
        self.configuration.Hide()
