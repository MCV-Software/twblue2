# -*- coding: cp1252 -*-
""" Module to handle global settings for TWBlue. """
import os
import logging
import platform
from pubsub import pub # type: ignore
from model import config_loader, paths
from view import messages

log = logging.getLogger("controller.appconfig")

# Name of file to store config in user folders.
MAINFILE = "twblue.conf"
# Name of config spec file, where all settings are specified in their default values.
MAINSPEC = "app-configuration.defaults"
# List with proxy types TWBlue does support.
proxyTypes = ["system", "http", "socks4", "socks4a", "socks5", "socks5h"]
# Singleton that will hold a reference to the global app config.
app = None
# Singleton that will hold a reference to the current keymap.
keymap=None
# Controls whether the keymap has been modified.
changed_keymap = False

def setup ():
    """ Inits global configuration for TWBlue or creates it in config path if does not exist. """
    global app
    if app != None:
        return
    log.debug("Loading global app settings...")
    # connect pubsub event response to invalid config issues.
    pub.subscribe(show_invalid_config_error, "core.invalid_configuration")
    app = config_loader.load_config(os.path.join(paths.config_path(), MAINFILE), os.path.join(paths.app_path(), "configspecs", MAINSPEC))
    log.debug("Loading keymap...")
#    global keymap
#    if float(platform.version()[:2]) >= 10 and app["settings"]["load_keymap"] == "default.keymap":
#        app["settings"]["load_keymap"] = "Windows 10.keymap"
#        app.write()
#        global changed_keymap
#        changed_keymap = True
#    keymap = config_loader.load_config(os.path.join(paths.config_path(), "keymap.keymap"), os.path.join(paths.app_path(), "keymaps/"+app['settings']['load_keymap']), copy=False, appconfig=True)

def show_invalid_config_error(appconfig: bool):
    """ Displays an error message if the configuration is invalid. """
    if appconfig:
        messages.invalid_configuration()