import unittest
from datetime import datetime as dt
from PythonRegistryDiffer.database import Database
from PythonRegistryDiffer.machine import Machine
from PythonRegistryDiffer.image import Image
from PythonRegistryDiffer.key import Key
from PythonRegistryDiffer.keyvalue import KeyValue


class TestCreateDatabase(unittest.TestCase):
    def test_create_database__memory_false_all_keys(self):
        db = Database(location=':memory:', auto_commit=False)
        self.assertEqual(db.location, ':memory:')
        self.assertEqual(db.auto_commit, False)
        self.assertEqual(db.hklm, True)
        self.assertEqual(db.hkcr, True)
        self.assertEqual(db.hkcu, True)
        self.assertEqual(db.hku, True)
        self.assertEqual(db.hkcc, True)

    def test_create_database_file_true_one_key(self):
        db = Database(location='newdatabase.db', auto_commit=True, hklm=False, hkcr=False, hkcu=False, hku=False,
                      hkcc=True)
        self.assertEqual(db.auto_commit, True)
        self.assertEqual(db.hklm, False)
        self.assertEqual(db.hkcr, False)
        self.assertEqual(db.hkcu, False)
        self.assertEqual(db.hku, False)
        self.assertEqual(db.hkcc, True)

    def test_create_database_memory_true_no_keys(self):
        with self.assertRaises(ValueError):
            Database(location=':memory:', auto_commit=True, hklm=False, hkcr=False, hkcu=False, hku=False, hkcc=False)


class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._dbm = Database(location=':memory:', auto_commit=True)
        cls._dbf = Database(location='testfile.db', auto_commit=True)

        cls._machine = Machine(ip='127.0.0.1', hostname='localhost')
        cls._image = Image(taken_time=dt.now(), label='test-image', machine=1)
        cls._keyvalue = KeyValue(name='KeyVal', type=2, data='data')
        cls._key = Key(key_path='HKEY_CLASSES_ROOT\\Test\\', modified=12345678, name='Test', values=[cls._keyvalue])

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self._dbf.open()
        self._dbm.open()

    def tearDown(self):
        self._dbf.close()
        self._dbm.close()
    # TODO: Third

    def test_open_database(self):
        self._dbm.open()
        self._dbf.open()

    def test_database_with_context_manager(self):
        with self._dbm as db:
            db.add_machine(machine=self._machine)
            # Not actually testing the add_machine here. Just making sure the context manager works.

        with self._dbf as db:
            db.add_machine(machine=self._machine)

    def test_database_insert_machine(self):
        self._dbf.add_machine(self._machine)
        self._dbm.add_machine(self._machine)

    def test_database_insert_image(self):
        self.test_database_insert_machine()
        self._dbf.add_image(self._image)

        self._dbm.add_machine(self._machine)
        self._dbm.add_image(self._image)

    def test_database_insert_key(self):
        self._dbf.add_key(1, self._key)

        self._dbm.add_machine(self._machine)
        self._dbm.add_image(self._image)
        self._dbm.add_key(1, self._key)

    def test_database_insert_key_value(self):
        self._dbf.add_key_value(1, self._keyvalue)

        self._dbm.add_machine(self._machine)
        self._dbm.add_image(self._image)
        self._dbm.add_key(1, self._key)
        self._dbm.add_key_value(1, self._keyvalue)

    def test_database_select_machine(self):
        self._dbm.add_machine(self._machine)

        xf = self._dbf.get_machine(1)
        xm = self._dbm.get_machine(1)

        self.assertEqual(xf.hostname, self._machine.hostname)
        self.assertEqual(xf.last_ip, self._machine.last_ip)
        self.assertEqual(xf.dbid, 1)

        self.assertEqual(xm.hostname, self._machine.hostname)
        self.assertEqual(xm.last_ip, self._machine.last_ip)
        self.assertEqual(xm.dbid, 1)

    def test_database_select_image(self):
        self._dbm.add_machine(self._machine)
        self._dbm.add_image(self._image)

        xf = self._dbf.get_image(1)
        xm = self._dbm.get_image(1)

        self.assertEqual(xf.machine, self._image.machine)
        self.assertEqual(str(xf.taken_time), str(self._image.taken_time))
        self.assertEqual(xf.label, self._image.label)
        self.assertEqual(xf.dbid, 1)

        self.assertEqual(xm.machine, self._image.machine)
        self.assertEqual(str(xm.taken_time), str(self._image.taken_time))
        self.assertEqual(xm.label, self._image.label)
        self.assertEqual(xm.dbid, 1)

    def test_database_select_key(self):
        self._dbm.add_machine(self._machine)
        self._dbm.add_image(self._image)
        self._dbm.add_key(1, self._key)
        self._dbm.add_key_value(1, self._keyvalue)

        xf = self._dbf.get_key(1)
        xm = self._dbm.get_key(1)

        xf.values = self._dbf.get_key_value_list(1)
        xm.values = self._dbm.get_key_value_list(1)


        self.assertEqual(xf.name, self._key.name)
        self.assertEqual(xf.modified, self._key.modified)
        self.assertEqual(xf.key_path, self._key.key_path)
        #self.assertEqual(xf.values, self._key.values) # this will never work. Can't compare the lists like this in python.
        # instead, I've added it into the key.__eq__()
        self.assertEqual(xf, self._key) # this will check name, modified, key_path, AND the actual key values directly.
        self.assertEqual(xf.has_values, self._key.has_values)
        self.assertEqual(xf.dbid, 1)

        self.assertEqual(xm.name, self._key.name)
        self.assertEqual(xm.modified, self._key.modified)
        self.assertEqual(xm.key_path, self._key.key_path)
        # self.assertEqual(xm.values, self._key.values) will never work, see above
        self.assertEqual(xm, self._key)
        self.assertEqual(xm.has_values, self._key.has_values)
        self.assertEqual(xm.dbid, 1)

    def test_database_select_key_value(self):
        self._dbm.add_machine(self._machine)
        self._dbm.add_image(self._image)
        self._dbm.add_key(1, self._key)
        self._dbm.add_key_value(1, self._keyvalue)

        xf = self._dbf.get_key_value(1)
        xm = self._dbm.get_key_value(1)

        self.assertEqual(xf.name, self._keyvalue.name)
        self.assertEqual(xf.type, self._keyvalue.type)
        self.assertEqual(xf.data, self._keyvalue.data)
        self.assertEqual(xf.dbid, 1)

        self.assertEqual(xm.name, self._keyvalue.name)
        self.assertEqual(xm.type, self._keyvalue.type)
        self.assertEqual(xm.data, self._keyvalue.data)
        self.assertEqual(xm.dbid, 1)

    # TODO: SELECT LIST OF X FUNCTION TESTING.
    # TODO: Test getting a key that doesn't exist.
    # TODO: Test different data types for KeyValues
    # TODO: Test large data for KeyValue; including data that's more than 1MB
