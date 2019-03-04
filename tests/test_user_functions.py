import unittest
import PythonRegistryDiffer.user_functions as exec


class TestUserFunctions(unittest.TestCase):

    def test_validate_arguments(self):
        self.assertEqual(exec.validate_arguments(), True)

    def test_new_database(self):
        self.assertEqual(exec.new_database(), True)

    def test_new_image(self):
        self.assertEqual(exec.new_image(), True)

    def test_list_images(self):
        self.assertEqual(exec.list_images(), True)

    def test_diff_images(self):
        self.assertEqual(exec.diff_images(), True)

    def test_load_db(self):
        self.assertEqual(exec.load_db(), True)

    def test_save_db(self):
        self.assertEqual(exec.save_db(), True)


if __name__ == '__main__':
    unittest.main()