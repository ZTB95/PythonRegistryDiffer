import os.path
import sqlite3
from . import sql
from .key import Key
from .keyvalue import KeyValue
from .image import Image
from .machine import Machine


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
        (You will almost always have autocommit turned on for this tool, but IMO default autocommit is a heresy. Maybe
        that's just my DBA background talking.)
        """
        self.auto_commit = auto_commit
        self.error_history = []
        self.hklm = hklm
        self.hkcu = hkcu
        self.hku = hku
        self.hkcr = hkcr
        self.hkcc = hkcc

        if self.hkeys == (False, False, False, False, False):
            raise ValueError('All HKEYs were set to false.')

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
        # TODO: exception stuff here. Need to see what exceptions happen first.

    @property
    def hkeys(self):
        hkey_tuple = (self.hklm, self.hkcu, self.hku, self.hkcr, self.hkcc)
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
        if self.location.lower() == 'memory':
            self.connection = sqlite3.connect(':memory:', detect_types=sqlite3.PARSE_DECLTYPES)
        else:
            self.connection = sqlite3.connect(self.location, detect_types=sqlite3.PARSE_DECLTYPES)

        # Create our cursor.
        self.cursor = self.connection.cursor()

        # Set up the proper HKEY Values if loaded db, or create the database and insert HKEYs if new db.
        if loaded:
            hkeys = self._run_and_fetch_all(sql.select_hkeys)
            self.hklm = bool(hkeys[0][1])
            self.hkcu = bool(hkeys[0][2])
            self.hku = bool(hkeys[0][3])
            self.hkcr = bool(hkeys[0][4])
            self.hkcc = bool(hkeys[0][5])
        else:
            self._create_database()
            self.cursor.execute(sql.insert_hkeys, self.hkeys)
            self.connection.commit()

    def close(self):
        if self.connection:

            if self.auto_commit:
                self.connection.commit()
            else:
                self.connection.rollback()

            self.connection.close()
            self.connection.close()
        self.connection = None  # In case self.close gets called before self.open, for whatever reason.

    def add_machine(self, machine):
        """
        Adds a Machine object to the database.
        :param machine: The Machine object to add to the database.
        :return: int ID of the machine
        """
        self.cursor.execute(sql.insert_into_machine, (
            machine.last_ip,
            machine.hostname
        ))

        if self.auto_commit:
            self.connection.commit()

        return self.get_newest_machine_id()

    def add_image(self, image):
        """
        Adds an image to the database. Note this doesn't add keys or values.
        :param image: The image object to add to the database.
        :return: int ID of the key
        """
        self.cursor.execute(sql.insert_into_regimage, (
            image.machine,  # TODO: Review having the parent ID inside of Image, but not the other objects.
            image.label,
            image.taken_time
        ))
        if self.auto_commit:
            self.connection.commit()

        new_image_id = self.get_newest_image_id()

        if image.keys is not None and len(image.keys) != 0:
            for key in image.keys:
                self.add_key(new_image_id, key)  # This function will then call add_key_value for each key's value.

        return new_image_id

    def add_key(self, image_id, key):
        """
        Adds a key to the database. Note that this doesn't add the key's values.
        :param image_id: The image to add the key to.
        :param key: The key object to add to the image.
        :return: int ID of the key
        """
        self.cursor.execute(sql.insert_into_regkey, (
            image_id,
            key.key_path,  # TODO: Review names for class properties. They're inconsistent.
            key.modified,
            key.name
        ))
        if self.auto_commit:
            self.connection.commit()
        new_key_id = self.get_newest_key_id()

        for key_value in key.values:
            self.add_key_value(new_key_id, key_value)

        return new_key_id

    def add_key_value(self, key_id, key_value):
        """
        Adds a (key) value to the specified PythonRegistryDiffer database.
        :param key_id: the id of the key that the key value belongs to.
        :param key_value: The key_value object
        :return: int ID of the key_value
        """
        self.cursor.execute(sql.insert_into_regkeyvalue, (
            key_id,
            key_value.name,
            key_value.type,
            key_value.data  # TODO: may have to send this in using the bytes class? Testing is needed.
        ))
        if self.auto_commit:
            self.connection.commit()

        return self.get_newest_key_value_id()

    def get_machine(self, machine_id):
        """
        Gets the specified machine from the Database.
        :param machine_id: The ID of the machine to get.
        :return: An instance of the Machine class.
        """
        mc = self._run_and_fetch_one(sql.select_all_from_machine_by_id, (machine_id,))
        new_machine = Machine(dbid=mc[0], ip=mc[1], hostname=mc[2])
        return new_machine

    def get_image(self, image_id):
        """
        Gets the specified image from the database.
        :param image_id: The database ID of the image to get.
        :return: Image instance or False
        """
        im = self._run_and_fetch_one(sql.select_all_from_regimage_by_id, (image_id,))
        new_image = Image(dbid=im[0], taken_time=im[3], label=im[2], machine=im[1])
        return new_image

    def get_key(self, key_id):
        """
        Gets the specified key from the database.
        :param key_id: The database ID of the key to get.
        :return: Key Instance or False
        """
        ky = self._run_and_fetch_one(sql.select_all_from_regkey_by_id, (key_id,))
        if ky is None:
            raise Exception('Zero results returned from query by ID. Check your input ID. 242 -> database.py. id: {0}'.format(key_id))
        new_key = Key(dbid=ky[0], key_path=ky[2], modified=ky[3], name=ky[4])
        return new_key

    def get_key_value(self, key_value_id):
        """
        Gets the key value from the database.
        :param key_value_id: The database ID of the key_value to get.
        :return: KeyValue instance or False
        """
        kv = self._run_and_fetch_one(sql.select_all_from_regkeyvalue_by_id, (key_value_id,))
        new_key_value = KeyValue(dbid=kv[0], name=kv[2], type=kv[3], data=kv[4])
        return new_key_value

    def get_image_list(self, machine_id=0):
        """
        Gets a list of images in the database.
        :param machine_id: set to a DBID to restrict to a specific Machine's Images.
        :return: A list of Images Instances.
        """
        im_list = self._run_and_fetch_all(sql.select_all_children_of_machine)
        new_image_list = []
        for item in im_list:
            new_image_list.append(Image(dbid=item[0], taken_time=item[3], label=item[2], machine=item[1]))
        return new_image_list

    def get_key_list(self, image_id):
        """
        Gets a list of key objects from the database.
        :param image_id: The DBID of the specific Images's Keys.
        :return: A list of Key instances
        """
        ky_list = self._run_and_fetch_all(sql.select_all_children_of_regimage_by_id, image_id)
        new_key_list = []
        for item in ky_list:
            new_key_list.append(Key(dbid=item[0], name=item[2], type=item[3], data=item[4]))

    def get_key_value_list(self, key_id):
        """
        Gets a list of key values from the database.
        :param key_id: The DBID of the specific Key's KeyValues.
        :return: A list of KeyValue instances
        """
        kv_list = self._run_and_fetch_all(sql.select_all_children_of_regkey_by_id, (key_id,))
        new_keyvalue_list = []
        for item in kv_list:
            new_keyvalue_list.append(KeyValue(dbid=item[0], name=item[2], type=item[3], data=item[4]))
        return new_keyvalue_list

    def get_newest_image_id(self):
        """
        Gets the ID of the newest image in the database by finding the highest ID.
        :return: int - the ID
        """
        return self._run_and_fetch_one(sql.select_newest_in_regimage)[0]

    def get_newest_machine_id(self):
        """
        Gets the ID of the newest machine in the database by finding the highest ID.
        :return: int - the ID
        """
        return self._run_and_fetch_one(sql.select_newest_in_machine)[0]

    def get_newest_key_id(self):
        """
        Gets the ID of the newest key in the database by finding the highest ID.
        :return: int - the ID
        """
        return self._run_and_fetch_one(sql.select_newest_in_regkey)[0]

    def get_newest_key_value_id(self):
        """
        Gets the ID of the newest key value in the database by finding the highest ID.
        :return: int - the ID
        """
        return self._run_and_fetch_one(sql.select_newest_in_regkeyvalue)[0]

    def get_count_of_machines_images_by_machine_id(self, machine_id):
        """
        Gets the number of images a machine has in the database.
        :param machine_id: The DBID of the machine who's images you want a count of.
        :return: int - The number of images the specified machine has.
        """
        return self._run_and_fetch_one(sql.select_number_of_images_a_machine_has, (machine_id,))[0]

    def _create_database(self):
        """
        Called by dunder init to create a new database.
        :return: None.
        """
        self.cursor.execute(sql.create_machine_table)
        self.cursor.execute(sql.create_image_table)
        self.cursor.execute(sql.create_key_table)
        self.cursor.execute(sql.create_key_value_table)
        self.cursor.execute(sql.create_hkeys_table)
        self.cursor.execute(sql.create_only_one_hkey_trigger)
        self.cursor.execute(sql.enforce_foreign_keys)
        self.cursor.execute(sql.insert_into_machine, ('127.0.0.1', 'localhost'))
        self.connection.commit()

    def _run_and_fetch_all(self, query, insert=None):
        """
        Runs a query and returns the fetchall result.
        :param query: The query to execute.
        :param insert: Optional. Insert values for the query, if any. Must be a tuple or None.
        :return: a list of the .fetchall() results
        """
        if insert is None:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        else:
            self.cursor.execute(query, insert)
            return self.cursor.fetchall()

    def _run_and_fetch_one(self, query, insert=None):
        """
        Runs a query and returns the fetchone result.
        :param query: The query to execute.
        :param insert: Optional. Insert values for the query, if any. Must be a tuple or None.
        :return: a list of the .fetchone() results
        """
        if insert is None:
            self.cursor.execute(query)
            return self.cursor.fetchone()
        else:
            self.cursor.execute(query, insert)
            return self.cursor.fetchone()
