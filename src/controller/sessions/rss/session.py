from typing import List, Any, cast
from pubsub import pub # type: ignore
from controller import config
from model.sessions import rss as model
from view.sessions.rss import dialogs as view

class Session(object):
    """ RSS Session controller class for TWblue"""

    def __init__(self, session_id: str):
        """ Class constructor

        :param session_id: session identifier.
        :type session_id: str
        """
        self.session_id = session_id

    def authorize_session(self):
        """ Starts the session authorization process

        This function is responsible to ask information about the session to the user, and calling to :py:func:`Session.create_session` if user has decided to create the session.
        """
        dlg = view.CreateSessionDialog()
        response: bool = dlg.get_response()
        if response == True:
            name: str = dlg.name.GetValue()
            self.create_session(name=name)
        dlg.Destroy()

    def create_session(self, name: str):
        """ Creates a session by instantiating a session model and configuring it

        :param name: Session name, as provided by the user in view.
        :type name: str
        """
        self.model = model.Session(session_id=self.session_id, name=name)
        self.model.prepare_path()
        self.model.get_configuration()
        self.model.login()
        session_data = dict(type=self.model.type, name="{name} ({type})".format(name=name, type="rss"), id=self.model.session_id)
        # Make name available as an attribute of the controller session so we can catch this for displaying it in the tree view later.
        self.name="{name} ({type})".format(name=name, type="rss")
        pub.sendMessage("sessionmanager.add_session_to_list", session_data=session_data)

    def create_buffers(self, force: bool = False):
        pub.sendMessage("core.create_account", session_id=self.session_id, buffer_title=self.name)
        # Avoid creating buffers if session is ignored and force is not set to True
        if self.session_id in config.app["sessions"]["ignored_sessions"] and force == False: # type: ignore
            return
        sites: List[str]  = list(self.model.settings["feeds"].keys())
        for site in sites:
            pub.sendMessage("core.create_buffer", buffer_type="RSSBuffer", session_type="rss", buffer_title=site, session_id=self.session_id, parent_tab=self.session_id, kwargs=dict(buffname=site, site=site))