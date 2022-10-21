#
# Compartment class
#

class Compartment:
    """A Pharmokinetic (PK) model

    Parameters
    ----------

    value: numeric, optional
        an example paramter

    """
    def __init__(self, volume, transition_rate):
    # NOTE: TRANSITION RATE IS CLEARANCE RATE FOR CENTRAL COMPARTMENTS 
    	# try: 
    	# 	self.volume = float(volume)
    	# 	self.transition_rate = float(transition_rate)
    	# except ValueError:
    	# 	raise TypeError('both volume and transition rate must be numeric.')
    	self.volume = volume
    	self.transition_rate = transition_rate
    def __str__(self):
        return self.name 

   