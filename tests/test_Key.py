import unittest
import datetime as dt
from PythonRegistryDiffer.Key import Key as k


class TestKey(unittest.TestCase):
    def testkey(self):
        date = dt.datetime.now()
        key = k(key_path='HKEY_CLASSES_ROOT\\Test\\', modified=12345678, name='Test', dbid=1)
        self.assertEqual(key.key_path, 'HKEY_CLASSES_ROOT\\Test\\')
        self.assertEqual(key.modified, 12345678)
        self.assertEqual(key.name, 'Test')
        self.assertEqual(key.dbid, 1)
        self.assertEqual(key.values, [])
        key = k(key_path='HKEY_CLASSES_ROOT\\Test\\', modified=12345678, name='Test', dbid=1, values=[1, 2, 3])
        self.assertEqual(key.values[1], 2)
        self.assertEqual(len(key.values), 3)


if __name__ == '__main__':
    unittest.main()
