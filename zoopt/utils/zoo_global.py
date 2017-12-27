
from random import Random

"""
This file records Global variables used in the algorithm
Author:
    Yuren Liu
"""

class Global:
    rand = None

    def __init__(self):
        # rand is the random object used by all files
        self.rand = Random()
        self.precision = 1e-17
        # rand.seed(100)

    # Set random seed
    def set_seed(self, seed):
        self.rand.seed(seed)
        return

    # Set precision, precision is used to judge whether two floats are equal
    def set_precision(self, my_precision):
        self.precision = my_precision
        return

gl = Global()
# constants
pos_inf = float('Inf')
neg_inf = float('-Inf')
nan = float('Nan')
