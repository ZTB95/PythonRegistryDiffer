import unittest
from PythonRegistryDiffer.key import Key as k


class TestKey(unittest.TestCase):
    def testkey_noval(self):
        # Test without values
        key = k(key_path='HKEY_CLASSES_ROOT\\Test\\', modified=12345678, name='Test', dbid=1)
        self.assertEqual(key.key_path, 'HKEY_CLASSES_ROOT\\Test\\')
        self.assertEqual(key.modified, 12345678)
        self.assertEqual(key.name, 'Test')
        self.assertEqual(key.dbid, 1)
        self.assertEqual(key.values, [])

    def testkey_withval(self):
        # Test with values
        key = k(key_path='HKEY_CLASSES_ROOT\\Test\\', modified=12345678, name='Test', dbid=1, values=[1, 2, 3])
        self.assertEqual(key.values[1], 2)
        self.assertEqual(len(key.values), 3)


if __name__ == '__main__':
    unittest.main()
