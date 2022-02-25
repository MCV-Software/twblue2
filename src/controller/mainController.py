# -*- coding: utf-8 -*-
""" Main controller for TWBlue.

This module is responsible to handle all requests sent by users as events and call corresponding models to retrieve data, which should later be presented to users via views.
"""
import webbrowser
from pubsub import pub # type: ignore
from model import mainModel, i18n
from view import mainWindow

class MainController(object):
    """ Main controller of TWBlue. """

    def __init__(self):
        """ Class constructor. """
        super(MainController, self).__init__()
        self.view = mainWindow.MainWindow()
        self.model = mainModel.MainModel()
        self.view.prepare()
        self.subscribe_core_events()
        self.view.Show()

    def subscribe_core_events(self):
        """ Subscribe core pubsub events to responses. """
        pub.subscribe(self.on_core_documentation, "core.documentation")
        pub.subscribe(self.on_core_changelog, "core.changelog")
        pub.subscribe(self.on_core_report_error, "core.report_error")
        pub.subscribe(self.on_core_visit_website, "core.visit_website")
        pub.subscribe(self.on_core_get_soundpacks, "core.get_soundpacks")
#        pub.subscribe(self.on_core_about, "core.about")

    def on_core_documentation(self):
        """ Callback function that opens the program documentation. """
        self.model.open_local_document("manual.html")

    def on_core_changelog(self):
        """ Callback function that opens the changelog documentation. """
        self.model.open_local_document("changelog.html")

    def on_core_report_error(self):
        webbrowser.open_new_tab("https://github.com/mcv-software/twblue/issues")

    def on_core_visit_website(self):
        url = "https://twblue.es"
        if i18n.lang == "es":
            url = "https://twblue.es/es"
        webbrowser.open_new_tab(url)

    def on_core_get_soundpacks(self):
        url = "https://twblue.es"
        if i18n.lang == "es":
            url = "https://twblue.es/es"
        webbrowser.open_new_tab(url+"/soundpacks")

