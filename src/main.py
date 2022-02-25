# -*- coding: utf-8 -*-
import wx # type: ignore
from controller import mainController
from model import i18n, logger

app = wx.App()
logger.setup()
i18n.setup("TWBlue")
c = mainController.MainController()
app.MainLoop()