# -*- coding: utf-8 -*-

class RSSBuffer(object):
    def __init__(self, session, name, *args, **kwargs):
        self.session = session
        self.name = name
        self.args = args
        self.kwargs = kwargs