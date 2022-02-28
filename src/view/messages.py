# -*- coding: utf-8 -*-
import wx

def exit_dialog():
    dlg = wx.MessageDialog(None, _("Do you really want to close TWBlue?"), _("Exit"), wx.YES_NO|wx.ICON_QUESTION)
    response = dlg.ShowModal()
    dlg.Destroy()
    if response == wx.ID_YES:
        return True
    return False

def invalid_configuration():
    dlg = wx.MessageDialog(None, _("The configuration file is invalid."), _("Error"), wx.ICON_ERROR)
    dlg.ShowModal()
    dlg.Destroy()