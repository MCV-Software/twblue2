# -*- coding: UTF-8 -*-
import wx # type: ignore
from pubsub import pub # type: ignore

class RSSBuffer(wx.Panel):
    def __init__(self, name: str, *args, **kwds):
        super(RSSBuffer, self).__init__(*args, **kwds)
        self.name = name
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        items_sizer = wx.WrapSizer(wx.HORIZONTAL)
        main_sizer.Add(items_sizer, 1, wx.EXPAND, 0)
        lbl_items = wx.StaticText(self, wx.ID_ANY, _("Items")) # type: ignore
        items_sizer.Add(lbl_items, 0, 0, 0)
        self.items = wx.ListBox(self, wx.ID_ANY, choices=[])
        items_sizer.Add(self.items, 0, 0, 0)
        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(buttons_sizer, 1, wx.EXPAND, 0)
        self.open = wx.Button(self, wx.ID_OPEN)
        self.open.SetDefault()
        self.open.Bind(wx.EVT_BUTTON, lambda event: pub.sendMessage("rss.open_link", item=self.items.GetSelection(), buffer_name=self.name))
        buttons_sizer.Add(self.open, 0, 0, 0)
        self.copy_link = wx.Button(self, wx.ID_ANY, _("Copy link")) # type: ignore
        self.copy_link.Bind(wx.EVT_BUTTON, lambda event: pub.sendMessage("rss.copy_link", item=self.items.GetSelection(), buffer_name=self.name))
        buttons_sizer.Add(self.copy_link, 0, 0, 0)
        self.SetSizer(main_sizer)
        main_sizer.Fit(self)
        self.Layout()