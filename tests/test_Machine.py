import unittest
from PythonRegistryDiffer.machine import Machine


class TestMachine(unittest.TestCase):
    def test_machine(self):
        mc = Machine(dbid=1, ip='127.0.0.1', hostname='localhost')
        self.assertEqual(mc.dbid, 1)
        self.assertEqual(mc.last_ip, '127.0.0.1')
        self.assertEqual(mc.hostname, 'localhost')
