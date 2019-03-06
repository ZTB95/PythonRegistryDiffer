import unittest
import datetime as dt
import PythonRegistryDiffer.Image as i


class TestImage(unittest.TestCase):
    def test___init__(self):
        date = dt.datetime.now()
        image = i.Image(taken_time=date, label='test image 1', machine='localhost', dbid=1)
        self.assertEqual(image.taken_time, date)
        self.assertEqual(image.label, 'test image 1')
        self.assertEqual(image.machine, 'localhost')
        self.assertEqual(image.dbid, 1)


if __name__ == '__main__':
    unittest.main()