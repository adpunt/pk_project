#
# Protocol class
#

class Protocol:
    """A Pharmokinetic (PK) protocol

    Parameters
    ----------

    value: numeric, optional
        an example paramter

    """
    def __init__(self, initial_dose: float, time: float, dose_func=lambda x, y: 0):
        if not callable(dose_func):
            raise TypeError('dose_func must be a callable function.')
        try: 
            # Test out dose_func to see if given two numeric inputs, it returns a numeric output
            val = dose_func(1, 2)
            float(val)
        except:
            raise TypeError('dose_func must take in two numeric inputs and return a numeric output.')
        self.dose_func = dose_func
        try:
            self.initial_dose = float(initial_dose)
            self.time = float(time)
        except ValueError:
            raise TypeError('initial_dose and time must be numeric.')

    def __str__(self):
        return self.name 

    @property
    def name(self) -> str:
        return '[initial_dose={0}, time={1}]'.format(self.initial_dose, self.time)
