# -*- coding: utf-8 -*-
""" Main RSS buffer controller """
import webbrowser
from view.sessions.rss.buffers import base as view
from model.sessions.rss.buffers import base as model
from model import output
from pubsub import pub

class RSSBuffer(object):

    def __init__(self, parent, session, buffname, *args, **kwargs):
        super(RSSBuffer, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.name = buffname
        self.session = session
        self.parent = parent
        self.view = None
        self.model = model.RSSBuffer(session=self.session.model, name=self.name, *self.args, **self.kwargs)
        self.subscribe_events()

    def subscribe_events(self):
        pub.subscribe(self.on_open_link, "rss.open_link")
        pub.subscribe(self.on_copy_link, "rss.copy_link")

    def unsubscribe_events(self):
        pub.unsubscribe(self.on_open_link, "rss.open_link")
        pub.unsubscribe(self.on_copy_link, "rss.copy_link")

    def create_gui(self):
        self.view = view.RSSBuffer(parent=self.parent, name=self.name)

    def get_items(self):
        items = self.model.get_items()
        for item in items:
            self.view.items.Append(item.get("title"))

    def on_open_link(self, buffer_name, item):
        if buffer_name == self.name:
            item = self.model.get_item(item)
            webbrowser.get("windows-default").open(item.get("url"))

    def on_copy_link(self, buffer_name, item):
        if buffer_name == self.name:
            item = self.model.get_item(item)
            output.copy(item.get("url"))
            output.speak(_("URL copied to clipboard"))