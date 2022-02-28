# -*- coding: utf-8 -*-
import wx # type: ignore
from controller import mainController, config
from model import i18n, logger

app = wx.App()
logger.setup()
i18n.setup("TWBlue")
config.setup()
c = mainController.MainController()
app.MainLoop()