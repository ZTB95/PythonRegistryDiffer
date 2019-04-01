import unittest
from PythonRegistryDiffer.database import Database
from PythonRegistryDiffer.machine import Machine
from PythonRegistryDiffer.image import Image
from PythonRegistryDiffer.key import Key
from PythonRegistryDiffer.keyvalue import KeyValue
from datetime import datetime as dt


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
        self.assertRaises(ValueError, Database(location=':memory:', auto_commit=True, hklm=False, hkcr=False,
                                               hkcu=False, hku=False, hkcc=False))


class TestDatabase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls._dbm = Database(location=':memory:', auto_commit=True)
        cls._dbf = Database(location='testfile.db', auto_commit=True)

    @classmethod
    def tearDown(cls):
        cls._dbm.close()
        cls._dbf.close()
        # just in case? Should ever actually need this. close() should be called if a context manager errors out

    # TODO: Third
    def test_open_database(self):
        self._dbm.open()
        self._dbf.open()
        self._machine = Machine(ip='127.0.0.1', hostname='localhost')
        self._image = Image(taken_time=dt.now(), label='test-image', machine=0)
        self._key = Key(key_path='HKEY_CLASSES_ROOT\\Test\\', modified=12345678, name='Test', dbid=1, values=[1, 2, 3])
        self._keyvalue = KeyValue(name='KeyVal', type=2, data='data', dbid=1)

    def test_database_with_context_manager(self):
        with self._dbm as db:
            db.add_machine(machine=self.mac)
            # Not actually testing the add_machine here. Just making sure the context manager works.

        with self._dbf as db:
            db.add_machine(machine=self.mac)
            # Not actually testing the add_machine here. Just making sure the context manager works.

    def test_database_insert_machine(self):
        self._dbf.add_machine(self._machine)
        self._dbm.add_machine(self._machine)

    def test_database_insert_image(self):
        self._dbf.add_image(self._image)
        self._dbm.add_image(self._image)

    def test_database_insert_key(self):
        self._dbf.add_key(self._key)
        self._dbm.add_key(self._key)

    def test_database_insert_key_value(self):
        self._dbf.add_key_value(self._keyvalue)
        self._dbm.add_key_value(self._keyvalue)

    def test_database_select_functions(self):
        pass

    def test_database_select_functions(self):
        pass

    def test_database_select_functions(self):
        pass

    def test_database_select_functions(self):
        pass

    def test_database_select_functions(self):
        pass

