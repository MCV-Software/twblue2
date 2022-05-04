import wx # type: ignore

class CreateSessionDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        super(CreateSessionDialog, self).__init__(parent=None, title=_("New RSS Session"), *args, **kwds)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_name = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(sizer_name, 1, wx.EXPAND, 0)
        label_name = wx.StaticText(self, wx.ID_ANY, _("Name for the RSS session"))
        sizer_name.Add(label_name, 0, 0, 0)
        self.name = wx.TextCtrl(self, wx.ID_ANY, "")
        sizer_name.Add(self.name, 0, 0, 0)
        buttons_sizer = wx.StdDialogButtonSizer()
        sizer.Add(buttons_sizer, 0, wx.ALIGN_RIGHT | wx.ALL, 4)
        self.ok = wx.Button(self, wx.ID_OK)
        self.ok.SetDefault()
        buttons_sizer.AddButton(self.ok)
        self.cancel = wx.Button(self, wx.ID_CANCEL)
        buttons_sizer.AddButton(self.cancel)
        buttons_sizer.Realize()
        self.SetSizer(sizer)
        sizer.Fit(self)
        self.SetAffirmativeId(self.ok.GetId())
        self.SetEscapeId(self.cancel.GetId())
        self.Layout()

    def get_response(self) -> bool:
        if self.ShowModal() == wx.ID_OK:
            return True
        return False