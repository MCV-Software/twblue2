from pubsub import pub
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

    def create_session(self):
        """ Starts the session creation process

        This function is responsible to ask information about the session to the user, and calling to :py:func:`Session.confirm_data` if user has decided to create the session.
        """
        dlg = view.CreateSessionDialog()
        response = dlg.get_response()
        if response == True:
            name = dlg.name.GetValue()
            self.confirm_data(name=name)
        dlg.Destroy()

    def confirm_data(self, name: str):
        """ Finish the session creation process by instantiating the session model and configuring it

        :param name: Session name, as provided by the user in view.
        :type name: str
        """
        self.model = model.Session(session_id=self.session_id, name=name)
        self.model.prepare_path()
        self.model.get_configuration()
        self.model.login()
        session_data = dict(type=self.model.type, name="{name} ({type})".format(name=name, type="rss"), id=self.model.session_id)
        pub.sendMessage("sessionmanager.add_session_to_list", session_data=session_data)

    def create_buffers(self)
        pub.sendMessage("core.create_buffer", buffer_type="RSSBuffer", session_type="rss", buffer_title="home", kwargs=dict(session=self.model, buffname="Home"))