import os.path
import sqlite3
from sqlite3 import Error as sqlerror
from .sql import SQL
from .key import Key
from .keyvalue import KeyValue
from .image import Image


class Database:
    """
    SQLite3 ORM for PythonRegistryDiffer.
    """
    def __init__(self, location, auto_commit=False, hklm=True, hkcu=True, hku=True, hkcr=True, hkcc=True):
        """
        Creates or loads a new database file (and object) with all of the tables this tool needs. Use with a context
        manager. If you're loading an existing database, you can ignore the hk%% items.
        :param location: the location for the database file. Can either be 'memory' or a filename to save to. If the
        file already exists, it will be loaded.
        :param auto_commit: Set to True if you want to automatically commit changes. Default value is False.
        """
        self.auto_commit = auto_commit
        self.error_history = []
        self.hklm = hklm
        self.hkcu = hkcu
        self.hku = hku
        self.hkcr = hkcr
        self.hkcc = hkcc
        self.location = location
        self.cursor = None

    def __enter__(self):
        # Get this value before we force it to be true.
        loaded = os.path.isfile(self.location)

        # Create the database connection.
        if self.location.lower == 'memory':
            self.connection = sqlite3.connect(':memory:')
        else:
            self.connection = sqlite3.connect(self.location)

        # Create our cursor.
        self.cursor = self.connection.cursor()

        # Set up the proper HKEY Values if loaded db, or insert them if new db.
        if loaded:
            # TODO: select the HKEY values
            pass
        else:
            # TODO: insert the HKEY values
            pass

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.rollback()
            self.connection.close()
        self.error_history.append(exc_val)
        return False  # Kill the context manager.

    @property
    def hklm(self):
        return self._hklm

    @hklm.setter
    def hklm(self, new):
        self._hklm = bool(new)

    @property
    def hkcu(self):
        return self._hkcu

    @hkcu.setter
    def hkcu(self, new):
        self._hkcu = bool(new)

    @property
    def hku(self):
        return self._hku

    @hku.setter
    def hku(self, new):
        self._hku = bool(new)

    @property
    def hkcr(self):
        return self._hkcr

    @hkcr.setter
    def hkcr(self, new):
        self._hkcr = bool(new)

    @property
    def hkcc(self):
        return self._hkcc

    @hkcc.setter
    def hkcc(self, new):
        self._hkcc = bool(new)

    def add_image(self, image):
        """
        Adds an image to the database. Note this doesn't add keys or values.
        :param image: The image object to add to the database.
        :return: A dictionary with the values 'errors' and 'data'. The 'data' tag will be the new image's database ID.
        """
        errors = []

        if self.auto_commit:
            self.commit()

    def add_key(self, image_id, key):
        """
        Adds a key to the database. Note that this doesn't add the key's values.
        :param image_id: The image to add the key to.
        :param key: The key object to add to the image.
        :return: A dictionary with the values 'errors' and 'data'. The 'data' tag will be the new key's database ID.
        """
        errors = []

        if self.auto_commit:
            self.commit()

    def add_key_value(self, key_id, key_value):
        """
        Adds a (key) value to the specified PythonRegistryDiffer database.
        :param key_id: the id of the key that the key value belongs to.
        :param key_value: The key_value object
        :return: A dictionary with the values 'errors' and 'data'. The 'data' tag will be the new key's database ID.
        """
        errors = []

        if self.auto_commit:
            self.commit()

    def get_image(self, image_id):
        """
        Gets the specified image from the database.
        :param image_id: The database ID of the image to get.
        :return: A dictionary with the values 'errors' and 'data'. 'data' will be an instance of the image class.
        """
        errors = []

        if self.auto_commit:
            self.commit()

    def get_key(self, key_id):
        """
        Gets the specified key from the database.
        :param key_id: The database ID of the key to get.
        :return: A dictionary with the values 'errors' and 'data'. 'data' will be an instance of the key class.
        """
        errors = []

        if self.auto_commit:
            self.commit()

    def get_key_value(self, key_value_id):
        """
        Gets the key value from the database.
        :param key_value_id: The database ID of the key_value to get.
        :return: A dictionary with the values 'errors' and 'data'. 'data' will be an instance of the key_value class.
        """
        errors = []

        if self.auto_commit:
            self.commit()

    def get_image_list(self):
        """
        Gets a list of images in the database.
        :return: A dictionary with the values 'errors' and 'data'. 'data' will be a list of image instances.
        """
        errors = []

        if self.auto_commit:
            self.commit()

    def get_key_list(self, image_id):
        """
        Gets a list of key objects from the database.
        :param image_id: The image ID of the keys to get.
        :return: A dictionary with the values 'errors' and 'data'. 'data' will be a list of key instances.
        """
        errors = []

        if self.auto_commit:
            self.commit()

    def get_key_value_list(self, key_id):
        """
        Gets a list of key values from the database.
        :param key_id: The key ID of the key values to get.
        :return: A dictionary with the values 'errors' and 'data'. 'data' will be a list of key instances.
        """
        errors = []

        if self.auto_commit:
            self.commit()
