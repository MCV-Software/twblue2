# -*- coding: utf-8 -*-
""" Logging setup for TWBlue

This module should be setup during startup of the application, and will create a logs folder, located in :py:func:`model.paths.logs_path`

There is also a special function that will debug all pubsub events when those are received.
"""
import sys
import os
import logging
from typing import Type, Any, Optional, cast, Dict
from types import TracebackType
from logging.handlers import RotatingFileHandler
from pubsub import pub # type: ignore
from . import paths

APP_LOG_FILE: str = "debug.log"
ERROR_LOG_FILE: str = "error.log"
MESSAGE_FORMAT: str = "%(asctime)s %(name)s %(levelname)s: %(message)s"
DATE_FORMAT: str = "%d-%m-%Y %H:%M:%S"
logger: logging.Logger = logging.getLogger()

def setup() -> None:
    """ configure logging in TWBlue by enabling and disabling handlers according to our needs. """
    global logger
    formatter: logging.Formatter = logging.Formatter(MESSAGE_FORMAT, datefmt=DATE_FORMAT)
    requests_log: logging.Logger = logging.getLogger("requests")
    requests_log.setLevel(logging.WARNING)
    urllib3: logging.Logger = logging.getLogger("urllib3")
    urllib3.setLevel(logging.WARNING)
    requests_oauthlib: logging.Logger = logging.getLogger("requests_oauthlib")
    requests_oauthlib.setLevel(logging.WARNING)
    oauthlib: logging.Logger = logging.getLogger("oauthlib")
    oauthlib.setLevel(logging.WARNING)
    logger.setLevel(logging.DEBUG)
    app_handler: RotatingFileHandler = RotatingFileHandler(os.path.join(paths.logs_path(), APP_LOG_FILE), mode="w", encoding="utf-8")
    app_handler.setFormatter(formatter)
    app_handler.setLevel(logging.DEBUG)
    logger.addHandler(app_handler)
    error_handler: logging.FileHandler = logging.FileHandler(os.path.join(paths.logs_path(), ERROR_LOG_FILE), mode="w", encoding="utf-8")
    error_handler.setFormatter(formatter)
    error_handler.setLevel(logging.ERROR)
    logger.addHandler(error_handler)
    pub.subscribe(log_pub_message, pub.ALL_TOPICS)

def log_pub_message(topicObj: Any = pub.AUTO_TOPIC, **mesgData: Dict[Any, Any]):
    """ Callback function that logs messages sent via pubsub.

    This function shoul not be called manually. It's just here for debugging purposes.

    :param topicObj: Topic to log messages from. By default the function will be subscribed to :py:data:`pubsub.pub.ALL_TOPICS` -which is the root topic.
    :type topicObj: str
    :param mesgData: Arguments passed to the topic.
    :type mesgData: dict
    """
    logger.debug("Received message for topic '%s': with args %r" % (topicObj.getName(), mesgData))

def setup_exception_handling() -> None:
    """ Special function that configures python to print exceptions to log files, as opposed to raise them in console.

    This is useful when running the application from a distribution folder and not in sources.

    This basically replaces the excepthook in the sys module with the function :py:func:`handle_exception`
    """
    sys.excepthook = handle_exception

def handle_exception(exc_type: Type[BaseException], exc_value: BaseException, exc_traceback: Optional[TracebackType]) -> Any:
    """ Logs all uncaught exceptions to a file. This should never be called directly. """
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, cast(TracebackType, exc_traceback))
        return
    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
