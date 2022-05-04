# -*- coding: utf-8 -*-
""" RSS Session model """
import feedparser # type: ignore
from model.sessions import base
from typing import List, Dict

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

    def order_buffer(self, buffer_name: str, data: List[Dict[str, str]], is_reversed: bool = False) -> int:
        added_items = 0
        if self.db.get(buffer_name) == None:
            self.db[buffer_name] = []
        objects = self.db[buffer_name]
        for i in data:
            # Determine if the object already exists in our local DB.
            item_found = next((item for item in objects if item["url"] == i["url"]), None)
            if item_found != None:
                continue
            if is_reversed == False:
                objects.append(i)
            else:
                objects.insert(0, i)
            added_items = added_items + 1
        self.db[buffer_name] = objects
        return added_items

    def get_items(self, site="", *args, **kwargs):
        site_rss = self.settings["feeds"].get(site, "")
        if site_rss == "":
            raise ValueError("Site name %s does not contain any rss feed" % (site))
        feed = feedparser.parse(site_rss)
        results = []
        for entry in feed.entries:
            results.append(dict(title=entry.get("title"), url=entry.get("link"), published=entry.get("published"), summary=entry.get("summary")))
        return results

    def add_site(self, site_name, site_url):
        content = feedparser.parse(site_url)
        if len(content.entries) > 0:
            self.settings["feeds"][site_name] = site_url
            self.settings.write()