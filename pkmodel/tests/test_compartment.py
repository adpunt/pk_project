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
            comp = pk.Compartment(1.0)
        with self.assertRaises(TypeError):
            comp = pk.Compartment("Hello", 1.0)
        with self.assertRaises(TypeError):
            comp = pk.Compartment(-1.0, 1.0)
        with self.assertRaises(TypeError):
            comp = pk.Compartment(1.0, -1.0)
        with self.assertRaises(TypeError):
            comp = pk.Compartment(0, 0)
        comp = pk.Compartment(1, 0)
        self.assertEquals(comp.name, '[v_p=1.0, q_p=0.0]')
        comp = pk.Compartment(4.0, 5.0)
        self.assertEquals(comp.name, '[v_p=4.0, q_p=5.0]')
