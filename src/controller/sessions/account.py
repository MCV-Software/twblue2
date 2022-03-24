# -*- coding: utf-8 -*-
from view.sessions import account as view
from pubsub import pub

class AccountBuffer(object):

    def __init__(self, parent, session, buffname, *args, **kwargs):
        super(AccountBuffer, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.session = session
        self.parent = parent
        self.name = buffname
        self.view = None

    def create_gui(self):
        self.view = view.Account(parent=self.parent, name=self.session.name)
