# -*- coding: utf-8 -*-

class RSSBuffer(object):
    def __init__(self, session, name, *args, **kwargs):
        self.session = session
        self.name = name
        self.args = args
        self.kwargs = kwargs

    def get_items(self):
        items = self.session.get_items(*self.args, **self.kwargs)
        new_items = self.session.order_buffer(buffer_name=self.name, data=items)
        added_items = self.session.db[self.name][-new_items:]
        return added_items

    def get_item(self, index):
        return self.session.db[self.name][index]