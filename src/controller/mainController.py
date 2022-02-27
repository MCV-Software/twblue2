# -*- coding: utf-8 -*-
""" Main controller for TWBlue.

This module is responsible to handle all requests sent by users as events and call corresponding models to retrieve data, which should later be presented to users via views.

Ideally, we are supposed to not include any logic within controllers, except when such kind of logic is necessary or is very minimum, thus making a own model to handle data is unnecessary. An example of this might be the functions :py:func:`MainController.on_core_visit_website`, :py:func:`MainController.on_core_report_error` and :py:func:`MainController.on_core_get_soundpacks`, which redirect users to a website.
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

    ### Callback functions.
    def on_core_documentation(self):
        """ Callback function that opens the program documentation in the user specified language. """
        self.model.open_local_document("manual.html")

    def on_core_changelog(self):
        """ Callback function that opens the changelog in the user specified language. """
        self.model.open_local_document("changelog.html")

    def on_core_report_error(self):
        """ Callback function that opens the issue reporting feature in github. """
        webbrowser.get("windows-default").open("https://github.com/mcv-software/twblue/issues")

    def on_core_visit_website(self):
        """ Callback function that opens the TWBlue website.

        If the language set in TWBlue is spanish, the spanish version of the site will be opened.
        """
        url = "https://twblue.es"
        if i18n.lang == "es":
            url = "https://twblue.es/es"
        webbrowser.get("windows-default").open(url)

    def on_core_get_soundpacks(self):
        """ Callback function that opens the soundpacks section in the TWBlue website:

        If the language set in TWBlue is spanish, the spanish version of the site will be opened.
        """
        url = "https://twblue.es"
        if i18n.lang == "es":
            url = "https://twblue.es/es"
        webbrowser.get("windows-default").open(url+"/soundpacks")

