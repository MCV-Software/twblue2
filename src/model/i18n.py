""" Localization support for TWBlue. """
import os
import locale
import gettext
import logging
from typing import cast
from . import paths

log = logging.getLogger("model.i18n")

lang: str = "en"

def setup(name: str, localepath: str = "locales", default_lang: str = "system"):
    """ Installs the gettext translation catalog corresponding to the passed language.

    :param name: Name of the application. This must match with the gettext domain name.
    :type name: str
    :param localepath: Path where the gettext catalogs can be found. Must be relative to :py:func:`model.paths.app_path`.
    :type localepath: str
    :param default_lang: two letter language code to attempt to install in the gettext catalog. Examples can be "en", "es", "ja", etc.
        If the special value "system" is passed, the default user language will be used.
    :type default_lang: str
    """
    global lang
    if default_lang == "system":
        lang = cast(str, locale.getdefaultlocale()[0])[:2]
    else:
        lang = default_lang
    os.environ["lang"] = lang
    log.debug("System detected language: {0}".format(lang,))
    gettext.install(name, localedir=os.path.join(paths.app_path(), localepath))