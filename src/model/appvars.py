# -*- coding: utf-8 -*-
from typing import Dict, List, Any

# Singleton object with all sessions defined in the program.

sessions: Dict[str, Any] = {}

class SessionNotFoundException(Exception): pass

def get_session(session_id: str) -> Any:
    global sessions
    result = sessions.get(session_id)
    if result == None:
        raise SessionNotFoundException()
    return result

def get_sessions() -> List[Any]:
    return list(sessions.values())