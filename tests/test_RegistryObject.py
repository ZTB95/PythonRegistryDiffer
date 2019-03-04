import unittest
import PythonRegistryDiffer.RegistryObject as ro


class TestRegistryObject(unittest.TestCase):

    def test___init__(self):
        with self.assertRaises(KeyError):
            ro.RegistryObject()
            ro.RegistryObject(**{})

    def test__create_new(self):
        with self.assertRaises(NotImplementedError):
            two_obj_dict = {'obj1': 1}
            ro.RegistryObject(**two_obj_dict)

    def test_create_from_database(self):
        with self.assertRaises(NotImplementedError):
            two_obj_dict = {'obj1': 1, 'obj2': 2}
            ro.RegistryObject(**two_obj_dict)


if __name__ == '__main__':
    unittest.main()