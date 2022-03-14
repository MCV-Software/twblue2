# -*- coding: utf-8 -*-
import logging
import threading

log = logging.getLogger("model.thread_utils")

def call_threaded(func, *args, **kwargs):
    #Call the given function in a daemonized thread and return the thread.
    def new_func(*a, **k):
        try:
            func(*a, **k)
        except:
            log.exception("Thread %d with function %r, args of %r, and kwargs of %r failed to run." % (threading.current_thread().ident, func, a, k))
    thread = threading.Thread(target=new_func, args=args, kwargs=kwargs)
    thread.daemon = True
    thread.start()
    return thread
