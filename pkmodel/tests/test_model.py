import unittest
import pkmodel as pk
import scipy.integrate
import pytest


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
        model = pk.Model(comp1, [comp2])
        self.assertEqual(model.name, 'v_c=1.0, cl=1.0, peripheral=[v_p=1.0, q_p=2.0], K_a=None')
        model = pk.Model(comp2, [comp1, comp3], 1.0)
        self.assertEqual(model.name, 'v_c=1.0, cl=2.0, peripheral=[v_p=1.0, q_p=1.0], [v_p=2.0, q_p=5.0], K_a=1.0')

    def test_add_compartment(self):
        """
        Tests the add_compartment function
        """
        comp1 = pk.Compartment(1.0, 1.0)
        comp2 = pk.Compartment(1.0, 2.0)
        comp3 = pk.Compartment(2.0, 5.0)
        model = pk.Model(comp1, [comp2])
        self.assertEqual(model.name, 'v_c=1.0, cl=1.0, peripheral=[v_p=1.0, q_p=2.0], K_a=None')
        with self.assertRaises(TypeError):
            model.add_compartment(1.0)
        model.add_compartment(comp3)
        self.assertEqual(model.name, 'v_c=1.0, cl=1.0, peripheral=[v_p=1.0, q_p=2.0], [v_p=2.0, q_p=5.0], K_a=None')

    def test_remove_compartment(self):
        """
        Tests the remove_compartment function
        """
        comp1 = pk.Compartment(1.0, 1.0)
        comp2 = pk.Compartment(1.0, 2.0)
        comp3 = pk.Compartment(2.0, 5.0)
        model = pk.Model(comp1, [comp2, comp3])
        self.assertEqual(model.name, 'v_c=1.0, cl=1.0, peripheral=[v_p=1.0, q_p=2.0], [v_p=2.0, q_p=5.0], K_a=None')
        with self.assertRaises(TypeError):
            model.remove_compartment(1.0)
        with self.assertRaises(ValueError):
            model.remove_compartment(comp1)
        model.remove_compartment(comp2)
        self.assertEqual(model.name, 'v_c=1.0, cl=1.0, peripheral=[v_p=2.0, q_p=5.0], K_a=None')

    def test_rhs(self):
        """
        Tests the function that generates the rhs of the PK modelling
        equations.
        """
        comp1 = pk.Compartment(1.0, 1.0)
        comp2 = pk.Compartment(1.0, 2.0)
        model = pk.Model(comp1, [comp2])
        protocol = pk.Protocol(1.0, 1.0)
        self.assertEqual(model.rhs(1, 1, protocol), [0.0, -1.0])
        protocol = pk.Protocol(2.0, 1.0, lambda t, y: 3 / (t + 1 / 4))
        self.assertEqual(model.rhs(1, 1, protocol), [0.0, 1.4])

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
