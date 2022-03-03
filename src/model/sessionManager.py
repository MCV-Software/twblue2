# -*- coding: utf-8 -*-
""" Module to perform session actions such as addition, removal or display of the global settings dialogue. """
import shutil
import time
import os
import logging
from model import output, paths, config_loader, appvars, sessions
from controller import config
from pubsub import pub

log = logging.getLogger("model.sessionManager")

class SessionManager(object):
    def __init__(self):
        """ Class constructor.

        Creates the SessionManager class controller, responsible for the accounts within TWBlue. From this dialog, users can add/Remove accounts, or load the global settings dialog.
        """
        super(SessionManager, self).__init__()
        log.debug("Setting up the session manager.")

    def get_session_list(self):
        sessionsList = []
        reserved_dirs = ["dicts"]
        log.debug("Filling the sessions list.")
        for i in os.listdir(paths.config_path()):
            if os.path.isdir(os.path.join(paths.config_path(), i)) and i not in reserved_dirs:
                log.debug("Adding session %s" % (i,))
                strconfig = "%s/session.conf" % (os.path.join(paths.config_path(), i))
                config_test = config_loader.load_config(strconfig)
                if len(config_test) == 0:
                    try:
                        log.debug("Deleting session %s" % (i,))
                        shutil.rmtree(os.path.join(paths.config_path(), i))
                        continue
                    except:
                        output.speak("An exception was raised while attempting to clean malformed session data. See the error log for details. If this message persists, contact the developers.",True)
                        os.exception("Exception thrown while removing malformed session")
                        continue
                if config_test.get("session", {}).get("type") != None:
                    name = _("{account_name} ({type})").format(account_name=config_test["session"]["name"], type=config_test["session"]["type"])
                    sessionsList.append(dict(type=config_test.get("session", {}).get("type"), id=i, name=name))
                else:
                    try:
                        log.debug("Deleting session %s" % (i,))
                        shutil.rmtree(os.path.join(paths.config_path(), i))
                    except:
                        output.speak("An exception was raised while attempting to clean malformed session data. See the error log for details. If this message persists, contact the developers.",True)
                        os.exception("Exception thrown while removing malformed session")
        return sessionsList

    def remove_account(self, index):
        shutil.rmtree(path=os.path.join(paths.config_path(), selected_account.get("id")), ignore_errors=True)

    def init_sessions(self, session_data):
        for s in session_data:
            tpe = s.get("type", "")
            id = s.get("id", "")
            if hasattr(sessions, tpe) == False:
                raise ValueError("Session of type %s does not exist." % (tpe))
            m = getattr(sessions, tpe)
            session = getattr(m, "Session")(session_id=id)
            session.get_configuration()
            appvars.sessions[id] = session