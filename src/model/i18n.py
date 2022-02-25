import os
import locale
import gettext
import logging
from . import paths

log = logging.getLogger("model.i18n")

lang = "en"

def setup(name, localepath="locales", default_lang="system"):
    global lang
    if default_lang == "system":
        lang = locale.getdefaultlocale()[0][:2]
    else:
        lang = default_lang
    os.environ["lang"] = lang
    log.debug("System detected language: {0}".format(lang,))
    gettext.install(name, localedir=os.path.join(paths.app_path(), localepath))