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
        if type(volume) not in [int, float]:
            raise TypeError('volume should be numeric')
        if type(transition_rate) not in [int, float]:
            raise TypeError('transition_rate should be numeric')
        self.volume = volume
        self.transition_rate = transition_rate


    def __str__(self):
        """Returns the name of the compartment as a string.
        """
        return self.name 
