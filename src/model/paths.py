# -*- coding: utf-8 -*-
import sys
import platform
import os
import glob
from typing import Optional, Union, cast
from platform_utils import paths as paths_ # type: ignore

# Current mode is portable, unless we detect an installer later.
mode: str = "portable"

# This will be the app's config directory, which would be different if the app is in either portable or installer mode.
directory: Union[str, os.PathLike] = ""

# A reference to the current filesystem encoding so we would deal better with special encodings under Windows.
fsencoding: str = sys.getfilesystemencoding()

def setup():
    global mode
    # Switch mode to installer if we find an "uninstall" file.
    if len(glob.glob("Uninstall.exe")) > 0:
        mode= "installed"

def app_path() -> str:
    """ Returns the path where the application files are located. """
    return paths_.app_path()

def config_path() -> str:
    """ Returns the app's config directory and creates it if it it doesn't exist yet.
    Normally, config directory is $HOME/.appname/config under Linux/OS X and %appdata%\\appname\\config in windows (installer mode), or just "app_path\\config" in portable mode."""
    global mode, directory
    path: str
    # Resolve first for non windows platforms, as should be in app config all the time.
    if platform.system() != "Windows":
        path = os.path.join(data_path(), "config")
    else:
        if mode == "portable":
            if directory != "":
                path = os.path.join(directory, "config")
            elif directory == "":
                path = os.path.join(app_path(), "config")
        elif mode == "installed":
            path = os.path.join(data_path(), "config")
    if not os.path.exists(path):
        os.mkdir(path)
    return path

def logs_path() -> str:
    global mode, directory
    path: str
    # Resolve first for non windows platforms, as should be in app config all the time.
    if platform.system() != "Windows":
        path = os.path.join(data_path(), "logs")
    else:
        if mode == "portable":
            if directory != "":
                path = os.path.join(directory, "logs")
            elif directory == "":
                path = os.path.join(app_path(), "logs")
        elif mode == "installed":
            path = os.path.join(data_path(), "logs")
    if not os.path.exists(path):
        os.mkdir(path)
    return path

def data_path(app_name: str = "TWBlue") -> str:
    data_path: str
    if platform.system() == "Windows":
        data_path = os.path.join(cast(Union[str, os.PathLike], os.getenv("AppData")), app_name)
    else:
        data_path = os.path.join(os.environ['HOME'], ".%s" % app_name)
    if not os.path.exists(data_path):
        os.mkdir(data_path)
    return data_path

def locale_path() -> str:
    return os.path.join(app_path(), "locales")

def sound_path() -> str:
    return os.path.join(app_path(), "sounds")