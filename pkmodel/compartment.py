class Compartment:
    """The Compartment class contains the building blocks of the PK
    model. Each compartment contains a volume and transition rate in
    and out of the compartmnet. Note that for central compartments, the
    transition rate represents the clearance rate.

    Attributes:
        volume: A float indicating the volume of that compartment.
        transition_rate: A float indicating either the rate [mL/h]
        between the central compartment and the peripheral
        compartment, in the case of a peripheral compartment, or the
        clearance/elimination rate, in the case of a central
        compartment.
    """

    def __init__(self, volume: float, transition_rate: float):
        # Argument validation
        if type(volume) not in [int, float] or volume <= 0:
            raise TypeError('volume should be a number greater than 0')
        if type(transition_rate) not in [int, float] or transition_rate < 0:
            raise TypeError('transition_rate should be a number greater than or equal to 0')
        self.volume = float(volume)
        self.transition_rate = float(transition_rate)

    def __str__(self):
        """Returns the name of the compartment as a string.
        """
        return self.name

    @property
    def name(self) -> str:
        return '[v_p={0}, q_p={1}]'.format(self.volume, self.transition_rate)
