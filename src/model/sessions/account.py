# -*- coding: utf-8 -*-
from controller import config

class Account(object):

    def __init__(self, session_id):
        self.session_id = session_id

    def autologin(self):
        if self.session_id in config.app["sessions"]["ignored_sessions"]:
            config.app["sessions"]["ignored_sessions"].remove(self.session_id)
        else:
            config.app["sessions"]["ignored_sessions"].append(self.session_id)
        config.app.write()