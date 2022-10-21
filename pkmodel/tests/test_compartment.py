import unittest
import pkmodel as pk


class CompartmentTest(unittest.TestCase):
    """
    Tests the :class:`Compartment` class.
    """
    def test_create(self):
        """
        Tests Compartment creation.
        """
        with self.assertRaises(TypeError):
            c = pk.Compartment(1.0)
        with self.assertRaises(TypeError):
            c = pk.Compartment("Hello", 1.0)
        with self.assertRaises(TypeError):
            c = pk.Compartment(-1.0, 1.0)
        with self.assertRaises(TypeError):
            c = pk.Compartment(1.0, -1.0)
        with self.assertRaises(TypeError):
            c = pk.Compartment(0, 0)
        c1 = pk.Compartment(1, 0)
        self.assertEquals(c1.name, '[volume=1.0, transition_rate=0.0]')
        c2 = pk.Compartment(4.0, 5.0)
        self.assertEquals(c2.name, '[volume=4.0, transition_rate=5.0]')