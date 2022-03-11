# -*- coding: utf-8 -*-
# Singleton object with all sessions defined in the program.

sessions = {}

class SessionNotFoundException(Exception): pass

def get_session(session_id):
    global sessions
    result = sessions.get(session_id)
    if result == None:
        raise SessionNotFoundException()
    return result

def get_sessions():
    return list(sessions.values())