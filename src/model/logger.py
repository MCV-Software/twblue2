# -*- coding: utf-8 -*-
import sys
import os
import logging
import paths
from logging.handlers import RotatingFileHandler

APP_LOG_FILE = 'debug.log'
ERROR_LOG_FILE = "error.log"
MESSAGE_FORMAT = "%(asctime)s %(name)s %(levelname)s: %(message)s"
DATE_FORMAT = "%d/%m/%Y %H:%M:%S"

def setup():
    formatter = logging.Formatter(MESSAGE_FORMAT, datefmt=DATE_FORMAT)
    requests_log = logging.getLogger("requests")
    requests_log.setLevel(logging.WARNING)
    urllib3 = logging.getLogger("urllib3")
    urllib3.setLevel(logging.WARNING)
    requests_oauthlib = logging.getLogger("requests_oauthlib")
    requests_oauthlib.setLevel(logging.WARNING)
    oauthlib = logging.getLogger("oauthlib")
    oauthlib.setLevel(logging.WARNING)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    app_handler = RotatingFileHandler(os.path.join(paths.logs_path(), APP_LOG_FILE), mode="w", encoding="utf-8")
    app_handler.setFormatter(formatter)
    app_handler.setLevel(logging.DEBUG)
    logger.addHandler(app_handler)
    error_handler = logging.FileHandler(os.path.join(paths.logs_path(), ERROR_LOG_FILE), mode="w", encoding="utf-8")
    error_handler.setFormatter(formatter)
    error_handler.setLevel(logging.ERROR)
    logger.addHandler(error_handler)

def setup_exception_handling():
    sys.excepthook = handle_exception

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
