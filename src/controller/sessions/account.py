# -*- coding: utf-8 -*-
from view.sessions import account as view
from model.sessions import account as model
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
        self.model = model.Account(session_id=self.session.session_id)
        self.subscribe_events()

    def create_gui(self):
        self.view = view.Account(parent=self.parent, name=self.session.name)

    def subscribe_events(self):
        pub.subscribe(self.on_autologin_changed, "account.autologin")
        pub.subscribe(self.on_login, "account.login")

    def unsubscribe_events(self):
        pub.unsubscribe(self.on_autologin_changed, "account.autologin")
        pub.subscribe(self.on_login, "account.login_session")

    def on_autologin_changed(self, name, autologin):
        if name != self.session.name:
            return
        self.model.autologin()

    def on_login(self, name):
        if self.session.name != name:
            return
        self.session.create_buffers(force=True)
        pub.sendMessage("core.update_buffers", session_id=self.session.session_id)