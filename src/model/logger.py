# -*- coding: utf-8 -*-
import sys
import os
import logging
from typing import Type, Any, Optional, cast
from types import TracebackType
from logging.handlers import RotatingFileHandler
from . import paths

APP_LOG_FILE: str = "debug.log"
ERROR_LOG_FILE: str = "error.log"
MESSAGE_FORMAT: str = "%(asctime)s %(name)s %(levelname)s: %(message)s"
DATE_FORMAT: str = "%d-%m-%Y %H:%M:%S"
logger: logging.Logger = logging.getLogger()

def setup() -> None:
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

def setup_exception_handling() -> None:
    sys.excepthook = handle_exception

def handle_exception(exc_type: Type[BaseException], exc_value: BaseException, exc_traceback: Optional[TracebackType]) -> Any:
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, cast(TracebackType, exc_traceback))
        return
    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
