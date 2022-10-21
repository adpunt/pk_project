import unittest
import pkmodel as pk
import pytest


class ProtocolTest(unittest.TestCase):
    """
    Tests the :class:`Protocol` class.
    """
    def test_create(self):
        """
        Tests Protocol creation.
        """
        with self.assertRaises(TypeError):
            protocol = pk.Protocol(1.0)
        with self.assertRaises(TypeError):
            protocol = pk.Protocol("hello", 1.0)
        with self.assertRaises(ValueError):
            protocol = pk.Protocol(0, 0)
        with self.assertRaises(ValueError):
            protocol = pk.Protocol(-1, 1)
        with self.assertRaises(ValueError):
            protocol = pk.Protocol(1, -1)
        with self.assertRaises(ValueError):
            protocol = pk.Protocol(1, 0)
        protocol = pk.Protocol(0, 1)
        self.assertEquals(protocol.name, '[initial_dose=0.0, time=1.0]')
        with self.assertRaises(TypeError):
            protocol = pk.Protocol(1, 1, 1)
        with self.assertRaises(TypeError):
            protocol = pk.Protocol(1, 1, "Hello")
        with self.assertRaises(TypeError):
            protocol = pk.Protocol(1, 1, lambda x: 1 + x)
        with self.assertRaises(TypeError):
            protocol = pk.Protocol(1, 1, lambda x: "hi")
        protocol = pk.Protocol(100, 10, lambda t, y: 1 / (t + 2))
        self.assertEquals(protocol.name, '[initial_dose=100.0, time=10.0]')
