# -*- coding: utf-8 -*-
""" Main window class

This is the main generic Window of TWBlue. It only contains the bare minimum of the application graphical components, such as a Menu Bar, which can be extended to support menus for specific networks, a tree view, responsible of saving all buffers for networks, and some methods to manipulate those buffers.
"""
import wx # type: ignore
import wx.adv # type: ignore
from pubsub import pub # type: ignore
from model import application

class MainWindow(wx.Frame):
    ### MENU
    def make_menu(self):
        """ Creates the menu bar for TWBlue.

        This is a base menu bar, which later can be extended via other network handlers in order to add specific menus which should be displayed in specific sites.
        """
        self.menu_bar = wx.MenuBar()

        # Application menu
        app = wx.Menu()
        self.manage_accounts = app.Append(wx.ID_ANY, _("&Manage accounts"))
        app.Bind(wx.EVT_MENU, lambda event: pub.sendMessage("core.manage_accounts"), self.manage_accounts)
        self.show_hide = app.Append(wx.ID_ANY, _("&Hide window"))
        app.Bind(wx.EVT_MENU, lambda event: pub.sendMessage("core.hide_gui"), self.show_hide)
        self.keystroke_editor = app.Append(wx.ID_ANY, _("&Edit keystrokes"))
        app.Bind(wx.EVT_MENU, lambda event: pub.sendMessage("core.keystroke_editor"), self.keystroke_editor)
        self.account_settings = app.Append(wx.ID_ANY, _("Account se&ttings"))
        app.Bind(wx.EVT_MENU, lambda event: pub.sendMessage("core.account_settings"), self.account_settings)
        self.global_settings = app.Append(wx.ID_PREFERENCES, _("&Global settings"))
        app.Bind(wx.EVT_MENU, lambda event: pub.sendMessage("core.global_settings"), self.global_settings)
        self.close = app.Append(wx.ID_EXIT, _("E&xit"))
        app.Bind(wx.EVT_MENU, lambda event: pub.sendMessage("core.close"), self.close)

        # audio menu
        audio = wx.Menu()
        self.seek_left = audio.Append(wx.ID_ANY, _("&Seek back 5 seconds"))
        audio.Bind(wx.EVT_MENU, lambda event: pub.sendMessage("audio.seek_left"), self.seek_left)
        self.seek_right = audio.Append(wx.ID_ANY, _("&Seek forward 5 seconds"))
        audio.Bind(wx.EVT_MENU, lambda event: pub.sendMessage("audio.seek_right"), self.seek_right)

        # Help Menu
        help = wx.Menu()
        self.doc = help.Append(wx.ID_ANY, _("&Documentation"))
        help.Bind(wx.EVT_MENU, lambda event: pub.sendMessage("core.documentation"), self.doc)
        self.sounds_tutorial = help.Append(wx.ID_ANY, _("Sounds &tutorial"))
        help.Bind(wx.EVT_MENU, lambda event: pub.sendMessage("core.sounds_tutorial"), self.sounds_tutorial)
        self.changelog = help.Append(wx.ID_ANY, _("&What's new in this version?"))
        help.Bind(wx.EVT_MENU, lambda event: pub.sendMessage("core.changelog"), self.changelog)
        self.check_for_updates = help.Append(wx.ID_ANY, _("&Check for updates"))
        help.Bind(wx.EVT_MENU, lambda event: pub.sendMessage("core.check_for_updates"), self.check_for_updates)
        self.report_error = help.Append(wx.ID_ANY, _("&Report an error"))
        help.Bind(wx.EVT_MENU, lambda event: pub.sendMessage("core.report_error"), self.report_error)
        self.visit_website = help.Append(wx.ID_ANY, _("{0}'s &website").format(application.name,))
        help.Bind(wx.EVT_MENU, lambda event: pub.sendMessage("core.visit_website"), self.visit_website)
        self.get_soundpacks = help.Append(wx.ID_ANY, _("Get soundpacks for TWBlue"))
        help.Bind(wx.EVT_MENU, lambda event: pub.sendMessage("core.get_soundpacks"), self.get_soundpacks)
        self.about = help.Append(wx.ID_ANY, _("About &{0}").format(application.name,))
        help.Bind(wx.EVT_MENU, lambda event: pub.sendMessage("core.about"), self.about)

        # Add all to the menu Bar
        self.menu_bar.Append(app, _("&Application"))
        self.menu_bar.Append(audio, _("&Audio"))
        self.menu_bar.Append(help, _("&Help"))

    ### MAIN
    def __init__(self):
        """ Class constructor.

        Creates the main Window of TWBlue.
        """
        super(MainWindow, self).__init__(None, -1, application.name, size=(1600, 1600))
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetTitle(application.name)
        self.make_menu()
        self.SetMenuBar(self.menu_bar)
        self.tree = wx.Treebook(self.panel, wx.ID_ANY)
        self.buffers = {}

    def prepare(self):
        self.sizer.Add(self.tree, 0, wx.ALL, 5)
        self.panel.SetSizer(self.sizer)
#  self.Maximize()
        self.sizer.Layout()
        self.SetClientSize(self.sizer.CalcMin())
#  print self.GetSize()

    def add_buffer(self, buffer, name):
        self.tree.AddPage(buffer, name)
        self.buffers[name] = buffer.GetId()

    def insert_buffer(self, buffer, name, pos):
        self.tree.InsertSubPage(pos, buffer, name)
        self.buffers[name] = buffer.GetId()

    def search_buffer(self, tab_name):
        for i in range(self.tree.GetPageCount()):
            if   self.tree.GetPage(i).name == tab_name:
                return i
