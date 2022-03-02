from pubsub import pub
from model.sessions import rss as model
from view.sessions.rss import dialogs as view

class Session(object):

    def __init__(self, session_id):
        self.session_id = session_id

    def create_session(self):
        dlg = view.CreateSessionDialog()
        response = dlg.get_response()
        if response == True:
            name = dlg.name.GetValue()
            self.confirm_data(name=name)
        dlg.Destroy()

    def confirm_data(self, name):
        self.model = model.Session(session_id=self.session_id, name=name)
        self.model.prepare_path()
        self.model.get_configuration()
        self.model.login()
        session_data = dict(type=self.model.type, name="{name} ({type})".format(name=name, type="rss"), id=self.model.session_id)
        pub.sendMessage("sessionmanager.add_session_to_list", session_data=session_data)