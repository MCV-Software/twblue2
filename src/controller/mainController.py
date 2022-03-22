# -*- coding: utf-8 -*-
""" Main controller for TWBlue.

This module is responsible to handle all requests sent by users as events and call corresponding models to retrieve data, which should later be presented to users via views.

Ideally, we are supposed to not include any logic within controllers, except when such kind of logic is necessary or is very minimum, thus making a own model to handle data is unnecessary. An example of this might be the functions :py:func:`MainController.on_core_visit_website`, :py:func:`MainController.on_core_report_error` and :py:func:`MainController.on_core_get_soundpacks`, which redirect users to a website.
"""
import webbrowser
from pubsub import pub # type: ignore
from model import mainModel, i18n, repeating_timer, thread_utils
from view import mainWindow
from controller.sessions import rss
from model import appvars

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
        self.start()

    def subscribe_core_events(self):
        """ Subscribe core pubsub events to responses. """
        pub.subscribe(self.on_core_documentation, "core.documentation")
        pub.subscribe(self.on_core_changelog, "core.changelog")
        pub.subscribe(self.on_core_report_error, "core.report_error")
        pub.subscribe(self.on_core_visit_website, "core.visit_website")
        pub.subscribe(self.on_core_get_soundpacks, "core.get_soundpacks")
        pub.subscribe(self.on_create_buffer, "core.create_buffer")
#        pub.subscribe(self.on_core_about, "core.about")

    def start(self):
        """ Starts the application logic by calling create_buffers in all sessions and setting the function to retrieve items in the buffers. """
        for session in appvars.get_sessions():
            session.create_buffers()
        thread_utils.call_threaded(self.update_buffers)
        self.update_schedule = repeating_timer.RepeatingTimer(60, self.update_buffers)
        self.update_schedule.start()

    def update_buffers(self):
        """ performs an update in all active buffers, by retrieving last posted items. """
        for b in self.model.buffers:
            b.get_items()

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

    def on_create_buffer(self, buffer_type="RSSBuffer", session_type="rss", session_id=None, buffer_title="", parent_tab=None, start=False, kwargs={}):
        """ Buffer creator function. This will configure a new buffer based in parameters sent in the pubsub event.

        :param buffer_type: type of buffer to create. This must exist as a class in the session you need to instantiate.
        :type buffer_type: str
        :param session_type: Session type needed to create the buffer.
        :type session_type: str
        :param session_id: ID of the session that requested this buffer.
        :type session_id: str
        :param buffer_title: Title of the buffer. This will be used in the GUI as the name of the tree item associated with the buffer.
        :type buffer_title: str
        :param parent_tab: Name of the tab this buffer belongs to.
        :type parent_tab: str
        :param start: Whether to start the buffer upon creation or wait until the buffer gets updated periodically.
        :type start: bool
        :param kwargs: List of arguments required by the buffer class.
        :type kwargs: dict
        """
        if session_type == "rss":
            m = rss
        if hasattr(m, buffer_type) == False:
            raise AttributeError("Session type %s.%s does not exist yet." % (session_type, buffer_type))
        # Retrieves the session that originated this event.
        session = appvars.get_session(session_id)
        buffer = getattr(m, buffer_type)(parent=self.view.tree, session=session, **kwargs)
        buffer.create_gui()
        self.model.buffers.append(buffer)
        if parent_tab == None:
            self.view.add_buffer(buffer.view, buffer_title)
        else:
            self.view.insert_buffer(buffer.view, buffer_title, parent_tab)

