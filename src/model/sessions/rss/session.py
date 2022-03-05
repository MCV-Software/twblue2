# -*- coding: utf-8 -*-
""" RSS Session model """
import feedparser
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

    def get_items(self, site=""):
        site_rss = self.settings["feeds"].get(site, "")
        if site_rss == "":
            raise ValueError("Site name %s does not contain any rss feed" % (site))
        return site_rss

    def add_site(self, site_name, site_url):
        content = feedparser.parse(site_url)
        if len(content.entries) > 0:
            self.settings["feeds"][site_name] = site_url
            self.settings.write()

    def get_site(self, site_name):
        return self.settings.get("feeds", {}).get(site_name, None)