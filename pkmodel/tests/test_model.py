import unittest
import pkmodel as pk


class ModelTest(unittest.TestCase):
    """
    Tests the :class:`Model` class.
    """
    def test_create(self):
        """
        Tests Model creation.
        """
        c1 = pk.Compartment(1.0, 1.0)
        c2 = pk.Compartment(1.0, 2.0)
        c3 = pk.Compartment(2.0, 5.0)
        with self.assertRaises(TypeError):
            m = pk.Model(1.0)
        with self.assertRaises(TypeError):
            m = pk.Model(1.0, 1.0)
        with self.assertRaises(TypeError):
            m = pk.Model(c1)
        with self.assertRaises(TypeError):
            m = pk.Model(c1, c2)
        m1 = pk.Model(c1, [c2])
        self.assertEqual(m1.name, 'central_volume=1.0, clearance_rate=1.0, peripheral_compartments=[volume=1.0, transition_rate=2.0], K_a=None')
        m2 = pk.Model(c2, [c1, c3], 1.0)
        self.assertEqual(m2.name, 'central_volume=1.0, clearance_rate=2.0, peripheral_compartments=[volume=1.0, transition_rate=1.0], [volume=2.0, transition_rate=5.0], K_a=1.0')


    def test_add_compartment(self):
        """
        Tests the add_compartment function
        """
        c1 = pk.Compartment(1.0, 1.0)
        c2 = pk.Compartment(1.0, 2.0)
        c3 = pk.Compartment(2.0, 5.0)
        m = pk.Model(c1, [c2])
        self.assertEqual(m.name, 'central_volume=1.0, clearance_rate=1.0, peripheral_compartments=[volume=1.0, transition_rate=2.0], K_a=None')
        with self.assertRaises(TypeError):
            m.add_compartment(1.0)
        m.add_compartment(c3)
        self.assertEqual(m.name, 'central_volume=1.0, clearance_rate=1.0, peripheral_compartments=[volume=1.0, transition_rate=2.0], [volume=2.0, transition_rate=5.0], K_a=None')

    def test_remove_compartment(self):
        """
        Tests the remove_compartment function
        """
        c1 = pk.Compartment(1.0, 1.0)
        c2 = pk.Compartment(1.0, 2.0)
        c3 = pk.Compartment(2.0, 5.0)
        m = pk.Model(c1, [c2, c3])
        self.assertEqual(m.name, 'central_volume=1.0, clearance_rate=1.0, peripheral_compartments=[volume=1.0, transition_rate=2.0], [volume=2.0, transition_rate=5.0], K_a=None')
        with.assertRaises(TypeError):
            m.remove_compartment(1.0)
        with.assertRaises(ValueError):
            m.remove_compartment(c1)
        m.remove_compartment(c2)
        self.assertEqual(m.name, 'central_volume=1.0, clearance_rate=1.0, peripheral_compartments=[volume=2.0, transition_rate=5.0], K_a=None')

    def test_rhs(self):
        """
        Tests the function that generates the rhs of the PK modelling
        equations.
        """
        c1 = pk.Compartment(1.0, 1.0)
        c2 = pk.Compartment(1.0, 2.0)
        m = pk.Model(c1, [c2])
        p1 = pk.Protocol(1.0, 1.0)
        rhs_output = lambda t, q: m.rhs(t, q, p1)
        assertEqual(rhs_output(1,1), [0.0, -1.0])
        assertEqual(rhs_output(2,5), [0.0, -5.0])

        test_fn = lambda t, y: 3 / (t + 1/4)
        p2 = pk.Protocol(2.0, 1.0, test_fn)
        rhs_output = lambda t, q: m.rhs(t, q, p2)
        assertEqual(rhs_output(1,1), [0.0, 1.4])
        assertEqual(rhs_output(0,0), [0.0, 12.0])
        

    def test_solve(self):
        """
        Tests the function that solves system of ODEs, determining
        how much of the drug in question is in each compartment at
        each timestep.

        IMPORTANT: This function is not working for me. No matter what
        inputs I use, scipy.integrate.solve_ivp gives raises a 
        ValueError.
        """
        c1 = pk.Compartment(1.0, 1.0)
        c2 = pk.Compartment(1.0, 2.0)
        m = pk.Model(c1, [c2])
        p = pk.Protocol(1.0, 1.0)
        self.assertRaises(ValueError):
            m.solve(p)
