import unittest
import PythonRegistryDiffer.userfunctions as exec
import tests.testing_prep as tp


class TestUserFunctions(unittest.TestCase):

    def test_new_database(self):
        tp.reset_all_changes()
        self.assertEqual(exec.new_database(), True)

    def test_new_image(self):
        tp.before_diff()
        self.assertEqual(exec.new_image(), True)

    def test_list_images(self):
        self.assertEqual(exec.list_images(), True)

    def test_diff_images(self):
        tp.before_second_diff()
        exec.new_image()
        self.assertEqual(exec.diff_images(), True)

    def test_load_db(self):
        self.assertEqual(exec.load_db(), True)

    def test_save_db(self):
        self.assertEqual(exec.save_db(), True)


if __name__ == '__main__':
    unittest.main()
