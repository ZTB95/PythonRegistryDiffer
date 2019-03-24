import os.path
import sqlite3
from . import sql
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

        # Defined in self.open() (or __enter__())
        self.cursor = None
        self.connection = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False  # Kill the context manager.
        # TODO: exception stuff here

    @property
    def hkeys(self):
        hkey_tuple = (self.hkcr, self.hkcu, self.hku, self.hkcr, self.hkcc)
        return hkey_tuple

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

    def open(self):
        # Get this value before we force it to be true.
        loaded = os.path.isfile(self.location)

        # Create the database connection.
        if self.location.lower == 'memory':
            self.connection = sqlite3.connect(':memory:')
        else:
            self.connection = sqlite3.connect(self.location)

        # Create our cursor.
        self.cursor = self.connection.cursor()

        # Set up the proper HKEY Values if loaded db, or create the database and insert HKEYs if new db.
        if loaded:
            # TODO: select the HKEY values
            pass
        else:
            self.cursor.execute(sql.create_database)
            self.cursor.execute(sql.insert_hkeys, self.hkeys)
            self.connection.commit()
            pass

    def close(self):
        if self.connection:
            self.connection.rollback()
            self.connection.close()

    def add_machine(self, machine):
        pass

    def add_image(self, image):
        """
        Adds an image to the database. Note this doesn't add keys or values.
        :param image: The image object to add to the database.
        :return: None
        """
        if self.auto_commit:
            self.connection.commit()

    def add_key(self, image_id, key):
        """
        Adds a key to the database. Note that this doesn't add the key's values.
        :param image_id: The image to add the key to.
        :param key: The key object to add to the image.
        :return: None
        """
        if self.auto_commit:
            self.connection.commit()

    def add_key_value(self, key_id, key_value):
        """
        Adds a (key) value to the specified PythonRegistryDiffer database.
        :param key_id: the id of the key that the key value belongs to.
        :param key_value: The key_value object
        :return: None
        """
        if self.auto_commit:
            self.connection.commit()

    def get_machine(self, machine_id):
        pass

    def get_image(self, image_id):
        """
        Gets the specified image from the database.
        :param image_id: The database ID of the image to get.
        :return: Image instance or False
        """

    def get_key(self, key_id):
        """
        Gets the specified key from the database.
        :param key_id: The database ID of the key to get.
        :return: Key Instance or False
        """

    def get_key_value(self, key_value_id):
        """
        Gets the key value from the database.
        :param key_value_id: The database ID of the key_value to get.
        :return: KeyValue instance or False
        """

    def get_image_list(self, machine_id=0):
        """
        Gets a list of images in the database.
        :param machine_id: set to a DBID to restrict to a specific Machine's Images.
        :return: A list of Images Instances.
        """

    def get_key_list(self, image_id):
        """
        Gets a list of key objects from the database.
        :param image_id: The DBID of the specific Images's Keys.
        :return: A list of Key instances
        """

    def get_key_value_list(self, key_id):
        """
        Gets a list of key values from the database.
        :param key_id: The DBID of the specific Key's KeyValues.
        :return: A list of KeyValue instances
        """

