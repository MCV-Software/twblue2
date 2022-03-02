# -*- coding: utf-8 -*-
from model.sessions import base

class Session(base.Session):
    def __init__(self, name, *args, **kwargs):
        super(Session, self).__init__(*args, **kwargs)
        self.config_spec = "rss.defaults"
        self.type = "rss"
        self.name = name

    def login(self):
        self.settings["session"]["name"] = self.name
        self.settings.write()