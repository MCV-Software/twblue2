# -*- coding: utf-8 -*-
""" Main model for TWBlue

This class is responsible for handling all logic required by the core application.
"""
import os
import webbrowser
from . import i18n, paths

class MainModel(object):

    def __init__(self):
        # Here we will store controllers for buffers.
        self.buffers = []

    def open_local_document(self, docname):
        documents_path = os.path.abspath(os.path.join(paths.app_path(), "documentation", i18n.lang))
        file = os.path.join(documents_path, docname)
        if os.path.exists(file) == False:
            file = os.path.abspath(os.path.join(paths.app_path(), "documentation", "en", docname))
        if os.path.exists(file) == False:
            raise FileNotFoundError("The document {} does not exist".format(file))
        webbrowser.open_new_tab(file)