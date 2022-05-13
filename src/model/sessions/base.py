# -*- coding: utf-8 -*-
""" A base class to be derived in possible new sessions for TWBlue and services."""
import os
import time
import logging
import sqlitedict # type: ignore
from model import paths, output, config_loader, application

log = logging.getLogger("sessionmanager.session")

class Session(object):
    """ Base session class. This needs to be derived and improved with new methods for every session created at TWBlue. """

    def __init__(self, session_id):
        """ Session constructor

        :param session_id: The name of the folder inside the config directory where the session is located. TWBlue will read configs from this folder.
        :type session_id: str.
        """
        super(Session, self).__init__()
        self.session_id = session_id
        self.logged = False
        self.settings = None
        self.db={}
        # Config specification file. Override this on every session which include a spec file.
        self.config_spec = "base.defaults"
        # Session type. Override this when creating new sessions.
        self.type = "base"

    @property
    def is_logged(self):
        """ Returns True if user has been logged into the current session. """
        return self.logged

    def get_configuration(self):
        """ Load settings for a session. If config doesn't exist for the current session, this function creates it. """
        file_ = os.path.join(paths.config_path(), self.session_id, "session.conf")
        log.debug("Creating config file %s" % (file_,))
        self.settings = config_loader.load_config(os.path.join(paths.config_path(), file_), os.path.join(paths.app_path(), "configspecs", self.config_spec))
        self.init_sound()
        self.load_persistent_data()

    def init_sound(self):
        """ Initializes the sound system for current session. """
        pass

    def login(self):
        """ LogsIn the user to the session. This function needs to be overwritten in every new session type. """
        pass

    def authorise(self):
        """ Runs any authorization flow required to retrieve login credentials for user in the current session.

        This needs to be overwritten in every new session class.
        """
        pass

    def get_sized_buffer(self, buffer, size, reversed=False):
        """ Returns a sublist with certain amount of items.

        :param buffer: A list of items of any kind.
        :type buffer: list
        :param size: The amount of items to be retrieved from the list.
        :type size: int
        :param reversed: Whether the list of items is being displayed in reverse order.
        :type reversed: bool
        """
        if isinstance(buffer, list) and size != -1 and len(buffer) > size:
            log.debug("Requesting {} items from a list of {} items. Reversed mode: {}".format(size, len(buffer), reversed))
            if reversed == True:
                return buffer[:size]
            else:
                return buffer[len(buffer)-size:]
        else:
            return buffer

    def save_persistent_data(self):
        """ Save the data to a persistent sqlite backed file in user config. """
        dbname=os.path.join(paths.config_path(), str(self.session_id), "cache.db")
        log.debug("Saving storage information...")
        # persist_size set to 0 means not saving data actually.
        if self.settings["general"]["persist_size"] == 0:
            if os.path.exists(dbname):
                os.remove(dbname)
            return
        # Let's check if we need to create a new SqliteDict object (when loading db in memory) or we just need to call to commit in self (if reading from disk).db.
        # If we read from disk, we cannot modify the buffer size here as we could damage the app's integrity.
        # We will modify buffer's size (managed by persist_size) upon loading the db into memory in app startup.
        if self.settings["general"]["load_cache_in_memory"] and isinstance(self.db, dict):
            log.debug("Opening database to dump memory contents...")
            db=sqlitedict.SqliteDict(dbname, 'c')
            for k in self.db.keys():
                sized_buff = self.get_sized_buffer(self.db[k], self.settings["general"]["persist_size"], self.settings["general"]["reverse_timelines"])
                db[k] = sized_buff
            db.commit(blocking=True)
            db.close()
            log.debug("Data has been saved in the database.")
        else:
            try:
                log.debug("Syncing new data to disk...")
                if hasattr(self.db, "commit"):
                    self.db.commit()
            except:
                output.speak(_("An exception occurred while saving the {app} database. It will be deleted and rebuilt automatically. If this error persists, send the error log to the {app} developers.").format(app=application.name),True)
                log.exception("Exception while saving {}".format(dbname))
                os.remove(dbname)

    def load_persistent_data(self):
        """Import data from a database file from user config. """
        log.debug("Loading storage data...")
        dbname=os.path.join(paths.config_path(), str(self.session_id), "cache.db")
        # If persist_size is set to 0, we should remove the db file as we are no longer going to save anything.
        if self.settings["general"]["persist_size"] == 0:
            if os.path.exists(dbname):
                os.remove(dbname)
            # Let's return from here, as we are not loading anything.
            return
        # try to load the db file.
        try:
            log.debug("Opening database...")
            db=sqlitedict.SqliteDict(os.path.join(paths.config_path(), dbname), 'c')
            # If load_cache_in_memory is set to true, we will load the whole database into memory for faster access.
            # This is going to be faster when retrieving specific objects, at the cost of more memory.
            # Setting this to False will read the objects from database as they are needed, which might be slower for bigger datasets.
            if self.settings["general"]["load_cache_in_memory"]:
                log.debug("Loading database contents into memory...")
                for k in db.keys():
                    self.db[k] = db[k]
                db.commit(blocking=True)
                db.close()
                log.debug("Contents were loaded successfully.")
            else:
                log.debug("Instantiating database from disk.")
                self.db = db
                # We must make sure we won't load more than the amount of buffer specified.
                log.debug("Checking if we will load all content...")
                for k in self.db.keys():
                    sized_buffer = self.get_sized_buffer(self.db[k], self.settings["general"]["persist_size"], self.settings["general"]["reverse_timelines"])
                    self.db[k] = sized_buffer
            if self.db.get("cursors") == None:
                cursors = dict(direct_messages=-1)
                self.db["cursors"] = cursors
        except:
            output.speak(_("An exception occurred while loading the {app} database. It will be deleted and rebuilt automatically. If this error persists, send the error log to the {app} developers.").format(app=application.name), True)
            log.exception("Exception while loading {}".format(dbname))
            try: 
                os.remove(dbname)
            except:
                pass

    def prepare_path(self):
        """ Creates user config path before attempting to create any settings file. """
        log.debug("Creating %s session in the %s path" % (self.type, self.session_id))
        path = os.path.join(paths.config_path(), self.session_id)
        if not os.path.exists(path):
            log.debug("Creating %s path" % (os.path.join(paths.config_path(), path),))
            os.mkdir(path)
