"""pkmodel is a Pharmokinetic modelling library.

It contains functionality for creating, solving, and visualising the solution
of Parmokinetic (PK) models

"""
# Import version info
from .version_info import VERSION_INT, VERSION  # noqa

import scipy

# Import main classes
from .model import Model    # noqa
from .protocol import Protocol    # noqa
from .compartment import Compartment     # noqa
