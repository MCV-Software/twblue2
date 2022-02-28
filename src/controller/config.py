# -*- coding: cp1252 -*-
import os
import logging
import platform
from pubsub import pub
from model import config_loader, paths
from view import messages

log = logging.getLogger("controller.appconfig")

MAINFILE = "twblue.conf"
MAINSPEC = "app-configuration.defaults"
proxyTypes = ["system", "http", "socks4", "socks4a", "socks5", "socks5h"]
app = None
keymap=None
changed_keymap = False

def setup ():
    global app
    if app != None:
        return
    log.debug("Loading global app settings...")
    # connect pubsub event response to invalid config issues.
    pub.subscribe(show_invalid_config_error, "core.invalid_configuration")
    app = config_loader.load_config(os.path.join(paths.config_path(), MAINFILE), os.path.join(paths.app_path(), "configspecs", MAINSPEC))
    log.debug("Loading keymap...")
    global keymap
    if float(platform.version()[:2]) >= 10 and app["settings"]["load_keymap"] == "default.keymap":
        app["settings"]["load_keymap"] = "Windows 10.keymap"
        app.write()
        global changed_keymap
        changed_keymap = True
    keymap = config_loader.load_config(os.path.join(paths.config_path(), "keymap.keymap"), os.path.join(paths.app_path(), "keymaps/"+app['settings']['load_keymap']), copy=False, appconfig=True)

def show_invalid_config_error(appconfig):
    if appconfig:
        messages.invalid_configuration()