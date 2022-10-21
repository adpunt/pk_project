class Protocol:
    """The Protocol class contains the dosing protocol for the PK
    model. The user can specify the initial dosage, timespan of the
    dosage, and an optional dosage function.

    Attributes:
        initial_dose: A float indicating initial dosage [ng].
        transition_rate: A float indicating either the rate [mL/h]
        between the central compartment and the peripheral
        compartment, in the case of a peripheral compartment, or the
        clearance/elimination rate, in the case of a central
        compartment.
    """

    def __init__(self, initial_dose, time, dose_func=lambda x, y: 0):
        # Argument validation
        if not callable(dose_func):
            raise TypeError('dose_func must be a callable function.')
        try:
            # Test out dose_func to see if given two numeric inputs, it returns a numeric output
            val = dose_func(1, 2)
            float(val)
        except Exception:
            raise TypeError('dose_func must take in two numeric inputs and return a numeric output.')
        self.dose_func = dose_func
        try:
            self.initial_dose = float(initial_dose)
            self.time = float(time)
        except ValueError:
            raise TypeError('initial_dose and time must be numeric.')
        if self.initial_dose < 0:
            raise ValueError('initial_dose must be greater than or equal to 0')
        if self.time <= 0:
            raise ValueError('time must be greater than 0')

    def __str__(self):
        """Returns the name of the protocol as a string.
        """
        return self.name

    @property
    def name(self) -> str:
        return '[initial_dose={0}, time={1}]'.format(self.initial_dose, self.time)

    # @property
    # def dose_func(self):
    #     return self.dose_func
