import unittest
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
        db = Database(location='newdatabase.db', auto_commit=True, hklm=False, hkcr=False, hkcu=False, hku=False)
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
        pass

    @classmethod
    def tearDown(cls):
        pass
