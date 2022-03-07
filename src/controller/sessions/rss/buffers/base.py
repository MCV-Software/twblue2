# -*- coding: utf-8 -*-
from view.sessions.rss.buffers import base as view
from model.sessions.rss.buffers import base as model

class RSSBuffer(object):

    def __init__(self, parent, session, buffname, *args, **kwargs):
        super(RSSBuffer, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.name = buffname
        self.session = session
        self.parent = parent
        self.view = None

    def create_gui(self):
        self.view = view.RSSBuffer(parent=self.parent)

