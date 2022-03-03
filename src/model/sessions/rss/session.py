# -*- coding: utf-8 -*-
""" RSS Session model """
from model.sessions import base

class Session(base.Session):
    """ Session model for RSS in TWBlue. 

        This class is responsible for the interaction with RSS feeds within TWBlue.
        """

    def __init__(self, name="", *args, **kwargs):
        """ Class constructor

        :param name: Name of the session. This will be used mainly during session manager fase.
        :type name: str.
        """
        super(Session, self).__init__(*args, **kwargs)
        self.config_spec = "rss.defaults"
        self.type = "rss"
        self.name = name

    def login(self):
        self.settings["session"]["name"] = self.name
        self.settings.write()