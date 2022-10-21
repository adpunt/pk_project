import pkmodel as pk
import scipy.integrate
import matplotlib.pyplot
import numpy

class Model:
    """A Pharmokinetic (PK) model

    Parameters
    ----------

    value: numeric, optional
        an example paramter

    """
    def __init__(self, central_compartment, peripheral_compartments, k_a=None):
        if not isinstance(central_compartment, pk.Compartment):
            raise TypeError('central_compartment must be type pk.Compartment')
        if type(peripheral_compartments) is not list:
            raise TypeError('peripheral_compartments must be a type of pk.Compartments')
        for c in peripheral_compartments:
            if not isinstance(c, pk.Compartment):
                raise TypeError('each peripheral compartment must be type pk.Compartment')
        if type(k_a) not in [float, int] and k_a is not None:
            raise TypeError('k_a must be type pk.Compartment')
        self.central_compartment = central_compartment
        self.peripheral_compartments = peripheral_compartments
        self.k_a = k_a

    def __str__(self):
        return self.name 

    @property
    def name(self) -> str:
        # Create a string of all peripheral compartments
        pc_str = ""
        for c in peripheral_compartments:
            pc_str = pc_str + str(c) + ", "
        pc_str = pc_str[:-2]
        if type(self.k_a) is None:
            return 'i.v. dosing model with '
            'central_volume={0}, clearance_rate={1}, peripheral_compartments={2}'.format(
                str(self.central_compartment.volume),
                str(self.central_compartment.transition_rate),
                pc_str,
            )
        else:
            return 'subcontinuous dosing model with '
            'central_volume={0}, clearance_rate={1}, peripheral_compartments={2}, K_a={3}'.format(
                str(self.central_compartment.volume),
                str(self.central_compartment.transition_rate),
                pc_str,
                str(self.k_a),
            )

    def add_compartment(self, c):
        if not isinstance(c, pk.Compartment):
            raise TypeError('new peripheral compartment must be type pk.Compartment.')
        self.peripheral_compartments.append(c)

    def remove_compartment(self, c):
        if not isinstance(c, pk.Compartment):
            raise TypeError('peripheral compartment to be removed must be type pk.Compartment.')
        if c in self.peripheral_compartments:
            self.peripheral_compartments.remove(c)
        else: 
            raise ValueError('peripheral compartment is not in list of compartments for this model.')

    def define_ode(self, t, q, protocol): 
        eqns = []
        q_c = q
        q_p = q
        q_0 = q
        if self.k_a is None:
            # i.v. dosing
            dqc_dt = protocol.dose_func(t, protocol.initial_dose) - q_c / self.central_compartment.volume * self.central_compartment.transition_rate
        else:
            # subcontinuous dosing
            dq0_dt = protocol.dose_func(t, protocol.initial_dose) - (self.k_a * q_0)
            eqns.append(dq0_dt)
            dqc_dt = self.k_a * q_c - q_c / self.central_compartment.volume * self.central_compartment.transition_rate
        for pc in self.peripheral_compartments:
            dqp_dt = pc.transition_rate * ((q_c / self.central_compartment.volume) - (q_p / pc.volume))
            eqns.append(dqp_dt)
        eqns.append(dqc_dt)
        return eqns


    def solve(self, protocol):
        if not isinstance(protocol, pk.Protocol):
            raise TypeError('protocol must be type pk.Protocol.')
        t_eval = numpy.linspace(0, protocol.time, 1000)
        if self.k_a is None:
            y0 = numpy.zeros(len(self.peripheral_compartments)+1)
        else:
            y0 = numpy.zeros(len(self.peripheral_compartments)+2)
        soln = scipy.integrate.solve_ivp(
            fun= lambda t, q: self.define_ode(t, q, protocol),
            t_span= [t_eval[0], t_eval[-1]],
            y0=y0, t_eval=t_eval
        )
        return soln


# I couldn't get this working even when I replaced the solve_ivp inputs with ones that were identical to the protocol (I used the same rhs function and model arguments as in the original protocol.py file)

