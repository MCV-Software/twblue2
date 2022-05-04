# -*- coding: utf-8 -*-
import os
from configobj import ConfigObj, ParseError # type: ignore
from validate import Validator, ValidateError # type: ignore
from pubsub import pub # type: ignore
from logging import getLogger

log = getLogger("config_utils")

class ConfigLoadError(Exception): pass

def load_config(config_path, configspec_path=None, copy=True, appconfig=True, *args, **kwargs):
    spec = ConfigObj(configspec_path, encoding='UTF8', list_values=False, _inspec=True)
    try:
        config = ConfigObj(infile=config_path, configspec=spec, create_empty=True, encoding='UTF8', *args, **kwargs)
    except ParseError:
        raise ConfigLoadError("Unable to load %r" % config_path)
    validator = Validator()
    validated = config.validate(validator, preserve_errors=False, copy=copy)
    if validated == True:
        config.write()
        return config
    else:
        log.exception("Error in config file: {0}".format(validated,))
        pub.sendMessage("core.invalid_configuration", appconfig=appconfig)

