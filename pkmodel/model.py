import pkmodel as pk
import scipy.integrate
import matplotlib.pylab as plt
import numpy


class Model:
    """A Pharmokinetic (PK) model class which takes in a central
    compartment, and a list of peripheral compartments and other
    relevant information with which to build a PK model. The user can
    then sovle and visualise this PK model using a dosing protocol.

    Attributes:
        central_component: A Compartment representing the central
            compartment of the PK model.
        peripheral_compartments: A list of Compartments representing
            the peripheral compartments of the PK model.
        k_a: An optional float representing the absorption rate in the
            case of subcontinuous dosing. The presence of this argument
            determines whether or not the dosing model is modelling
            I.V. or subcontinous dosing.
    """
    def __init__(self, central_compartment, peripheral_compartments, k_a=None):
        # Argument validation
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
        if k_a is not None:
            self.k_a = float(k_a)
        else:
            self.k_a = None

    def __str__(self):
        """Returns the name of the model as a string.
        """
        return self.name

    @property
    def name(self) -> str:
        # Create a string of all peripheral compartments
        pc_str = ""
        for c in self.peripheral_compartments:
            pc_str = pc_str + str(c) + ", "
        pc_str = pc_str[:-2]
        # Piece the rest of the string together
        if type(self.k_a) is None:
            return 'v_c={0}, cl={1}, peripheral={2}'.format(
                str(self.central_compartment.volume),
                str(self.central_compartment.transition_rate),
                pc_str,
            )
        else:
            return 'v_c={0}, cl={1}, peripheral={2}, K_a={3}'.format(
                str(self.central_compartment.volume),
                str(self.central_compartment.transition_rate),
                pc_str,
                str(self.k_a),
            )

    def add_compartment(self, new_compartment):
        """Add a peripheral compartment to the PK model.

        Args:
            new_compartment: An instance of type compartment to be
                added to the PK model as a peripheral compartment.

        Raises:
            TypeError: If new_compartment is not of type Compartment.
        """
        if not isinstance(new_compartment, pk.Compartment):
            raise TypeError('new peripheral compartment must be type pk.Compartment.')
        self.peripheral_compartments.append(new_compartment)

    def remove_compartment(self, delete_compartment):
        """Add a peripheral compartment to the PK model.

        Args:
            new_compartment: An instance of type compartment to be
                removed from the existing list of peripheral
                compartments in the PK model.

        Raises:
            TypeError: If delete_compartment is not of type
                Compartment.
        """
        if not isinstance(delete_compartment, pk.Compartment):
            raise TypeError('peripheral compartment to be removed must be type pk.Compartment.')
        if delete_compartment in self.peripheral_compartments:
            self.peripheral_compartments.remove(delete_compartment)
        else:
            raise ValueError('peripheral compartment is not in list of compartments for this model.')

    def rhs(self, t, q, protocol):
        """Returns the right-hand-sides of a system of equation of
        Ordinary Differential Equations (ODEs) representing the given
        PK model.

        Args:
            t: float representing the dependent variable, time in this
                case
            q: float representing the time-dependent variable, drug
                quantity in this case

        Returns:
            List of equations representing the rhs of the PK model
            given in terms of t and q.
        """
        eqns = []
        q_c = q
        q_p = q
        q_0 = q
        v_c = self.central_compartment.volume
        q_c = self.central_compartment.transition_rate
        if not self.k_a:
            # I.V. dosing
            dqc_dt = protocol.dose_func(t,q) - (q_c / v_c) * q_c
        else:
            # Subcontinuous dosing
            dq0_dt = protocol.dose_func(t,q) - (self.k_a * q_0)
            eqns = (dq0_dt)
            dqc_dt = (self.k_a * q_c) - (q_c / v_c) * q_c
        # Calculate transitions which will be used in both dqc_dt and dqp_dt
        res_p = []
        for pc in self.peripheral_compartments:
            dqp_dt = pc.transition_rate * ((q_c / v_c) - (q_p / pc.volume))
            res_p.append(dqp_dt)
        res = dqc_dt
        for p in res_p:
            res += p
        return res

    def plot_sol(self, sol):
        """Plots the solution to the PK model.

        Args:
            sol: An object of type scipy.integrate._ivp.ivp.OdeResult
            that represents the quantities of a drug in a given
            compartment over time.
        """
        fig = plt.figure()
        plt.plot(sol.t, sol.y[0, :], label=self.name + '- q_c')
        plt.plot(sol.t, sol.y[1, :], label=self.name + '- q_protocol1')
        plt.legend()
        plt.ylabel('drug mass [ng]')
        plt.xlabel('time [h]')
        plt.show()

    def solve(self, protocol):
        """Solves the PK model given a protocol, using scipy's solve_ivp
        function.

        Args:
            protocol: Protocol object representing the dosing protocol
                that will be used to solve the PK model.

        Returns:
            A solution to the PK model representing the drug quantitiy
            in each compartment over time.
        """
        # Argument validation
        if not isinstance(protocol, pk.Protocol):
            raise TypeError('protocol must be type pk.Protocol.')
        # Create a list of timesteps
        t_eval = numpy.linspace(0, protocol.time, 1000)
        # Determine how many initial conditions to set
        if not self.k_a:
            y0 = numpy.zeros(len(self.peripheral_compartments) + 1)
        else:
            y0 = numpy.zeros(len(self.peripheral_compartments) + 2)
        y0[0] = protocol.initial_dose
        # Solve ODE based on system of equations, timespan, and initial conditions
        sol = scipy.integrate.solve_ivp(
            fun=lambda t, y: self.rhs(t, y, protocol),
            t_span=[t_eval[0], t_eval[-1]],
            y0=y0, t_eval=t_eval
        )
        self.plot_sol(sol)
        return sol
