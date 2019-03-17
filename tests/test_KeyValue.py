import unittest
from PythonRegistryDiffer.keyvalue import KeyValue as kv


class TestKeyValue(unittest.TestCase):
    def test_KvInit(self):
        keyvalue = kv(name='KeyVal', type=2, data='data', dbid=1)
        self.assertEquals(keyvalue.name, 'KeyVal')
        self.assertEqual(keyvalue.type, 2)
        self.assertEqual(keyvalue.data, 'data')
        self.assertEqual(keyvalue.dbid, 1)


if __name__ == '__main__':
    unittest.main()
