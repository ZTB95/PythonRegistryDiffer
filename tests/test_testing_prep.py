import unittest
import PythonRegistryDiffer.testing_prep as tp


class TestTestingPrep(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDown(cls):
        tp.reset_all_changes()

    def test_reset_all_changes(self):
        self.assertEqual(tp.reset_all_changes(), 'All test keys deleted.')

    def test_before_diff(self):
        self.assertEqual(tp.before_diff(), 'Ready to test first diff.')

    def test_before_second_diff(self):
        with self.assertRaises(WindowsError):
            tp.before_second_diff()

        tp.before_diff()
        self.assertEqual(tp.before_second_diff(), 'Ready to test second diff.')


if __name__ == '__main__':
    unittest.main()