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
        comp1 = pk.Compartment(1.0, 1.0)
        comp2 = pk.Compartment(1.0, 2.0)
        comp3 = pk.Compartment(2.0, 5.0)
        with self.assertRaises(TypeError):
            model = pk.Model(1.0)
        with self.assertRaises(TypeError):
            model = pk.Model(1.0, 1.0)
        with self.assertRaises(TypeError):
            model = pk.Model(comp1)
        with self.assertRaises(TypeError):
            model = pk.Model(comp1, comp2)
        model1 = pk.Model(comp1, [comp2])
        self.assertEqual(model1.name, 'central_volume=1.0, \
            clearance_rate=1.0, \
            peripheral_compartments=[volume=1.0, \
            transition_rate=2.0], \
            K_a=None')
        model2 = pk.Model(comp2, [comp1, comp3], 1.0)
        self.assertEqual(model2.name, 'central_volume=1.0, \
            clearance_rate=2.0, \
            peripheral_compartments=[volume=1.0, \
            transition_rate=1.0], \
            [volume=2.0, transition_rate=5.0], \
            K_a=1.0')


    def test_add_compartment(self):
        """
        Tests the add_compartment function
        """
        comp1 = pk.Compartment(1.0, 1.0)
        comp2 = pk.Compartment(1.0, 2.0)
        comp3 = pk.Compartment(2.0, 5.0)
        model = pk.Model(comp1, [comp2])
        self.assertEqual(model.name, 'central_volume=1.0, \
            clearance_rate=1.0, \
            peripheral_compartments=[volume=1.0, \
            transition_rate=2.0], \
            K_a=None')
        with self.assertRaises(TypeError):
            model.add_compartment(1.0)
        model.add_compartment(comp3)
        self.assertEqual(model.name, 'central_volume=1.0, \
            clearance_rate=1.0, \
            peripheral_compartments=[volume=1.0, \
            transition_rate=2.0], \
            [volume=2.0, transition_rate=5.0], \
            K_a=None')


    def test_remove_compartment(self):
        """
        Tests the remove_compartment function
        """
        comp1 = pk.Compartment(1.0, 1.0)
        comp2 = pk.Compartment(1.0, 2.0)
        comp3 = pk.Compartment(2.0, 5.0)
        model = pk.Model(comp1, [comp2, comp3])
        self.assertEqual(model.name, 'central_volume=1.0, \
            clearance_rate=1.0, \
            peripheral_compartments=[volume=1.0, \
            transition_rate=2.0], \
            [volume=2.0, transition_rate=5.0], \
            K_a=None')
        with self.assertRaises(TypeError):
            model.remove_compartment(1.0)
        with self.assertRaises(ValueError):
            model.remove_compartment(comp1)
        model.remove_compartment(comp2)
        self.assertEqual(model.name, 'central_volume=1.0, \
            clearance_rate=1.0, \
            peripheral_compartments=[volume=2.0, \
            transition_rate=5.0], \
            K_a=None')


    def test_rhs(self):
        """
        Tests the function that generates the rhs of the PK modelling
        equations.
        """
        comp1 = pk.Compartment(1.0, 1.0)
        comp2 = pk.Compartment(1.0, 2.0)
        model = pk.Model(comp1, [comp2])
        protocol1 = pk.Protocol(1.0, 1.0)
        rhs_output = lambda t, q: model.rhs(t, q, protocol1)
        assertEqual(rhs_output(1,1), [0.0, -1.0])
        assertEqual(rhs_output(2,5), [0.0, -5.0])
        protocol2 = pk.Protocol(2.0, 1.0, lambda t, y: 3 / (t + 1/4))
        rhs_output = lambda t, q: model.rhs(t, q, protocol2)
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
        comp1 = pk.Compartment(1.0, 1.0)
        comp2 = pk.Compartment(1.0, 2.0)
        model = pk.Model(comp1, [comp2])
        protocol = pk.Protocol(1.0, 1.0)
        with self.assertRaises(ValueError):
            model.solve(protocol)
