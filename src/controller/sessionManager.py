# -*- coding: cp1252 -*-
""" Controller for session manager """
import time
import wx
from typing import Dict
from pubsub import pub
from model import sessionManager as model
from view import sessionManager as view
from controller import sessions

class SessionManager(object):
    """ Session manager controller class

    This class should be instantiated every time the user needs to manage accounts within TWBlue and it is responsible to manage the dialog for accounts, as well as create or delete any session requested by users.
    """

    def __init__(self, started: bool = False):
        """ Class constructor

        :param started: Indicates whether TWBlue has already been started or not.
        :type started: bool.
        """
        super(SessionManager, self).__init__()
        self.started = started
        self.view = view.SessionManagerWindow()
        self.model = model.SessionManager()
        pub.subscribe(self.on_new_account, "sessionmanager.new_account")
        pub.subscribe(self.on_add_session_to_list, "sessionmanager.add_session_to_list")
#        pub.subscribe(self.remove_account, "sessionmanager.remove_account")
#        if self.started == False:
#            pub.subscribe(self.configuration, "sessionmanager.configuration")
#        else:
        self.view.hide_configuration()
        # Store a temporary copy of new and removed sessions, so we will perform actions on them during call to on_ok.
        self.new_sessions = {}
        self.removed_sessions = []
        self.sessions = []

    def start(self):
        """ Starts work on session manager module.

        This function should be called right after the controller has been created.

        here, all sessions that are actually valid will be added to the view's list and displayed to the user.
        """
        self.sessions = self.model.get_session_list()
        for session in self.sessions:
            name = session.get("name", "")
            self.view.list.Append(name)
        self.view.ShowModal()
        self.view.Destroy()

    def on_new_account(self, type: str):
        """ Starts creation of a new session.

        This function inits creation of a new session. New sessions will be created in the config path returned by :py:func:`model.paths.config_path` and will have a generated name consisting in random numbers.

        :param type: Type of the session to create. All valid sessions must exist in :py:mod:`controller.sessions`
        :type type: str
        """
        # Generate a random string to be used as a name for the folder.
        location = str(time.time())[-6:]
        # Raise an error if session type is not present.
        if not hasattr(sessions, type):
            raise ValueError("Session type %s does not exist." % (type))
        m = getattr(sessions, type)
        s = getattr(m, "Session")(location)
        s.create_session()

    def on_add_session_to_list(self, session_data: Dict[str, str]):
        """ Ads a new session to the list of available sessions in the manager

        This will add automatically the new session to the list of sessions in the view as well.

        :param session_data: a dictionary containing keys type, name and id, with session type, session name and session identifier.
        :type session_data: dict
        """
        self.sessions.append(session_data)
        self.view.list.Append(session_data.get("name", ""))