"""
This module contains the class Global.

Author:
    Yu-Ren Liu
"""

from random import Random


class Global:
    """
    This class defines global variables used in the algorithm.
    """
    rand = None

    def __init__(self):
        """
        Initialization, includes rand and precision.
        """
        # rand is the random object used by all files
        self.rand = Random()
        self.precision = 1e-17
        # rand.seed(100)

    def set_seed(self, seed):
        """
        Set random seed.

        :param seed: random seed
        :return: no return
        """
        self.rand.seed(seed)
        return

    def set_precision(self, my_precision):
        """
        Set precision, precision is used to judge whether two floats are equal.

        :param my_precision: precision
        :return: no return
        """
        self.precision = my_precision
        return

gl = Global()
# constants
pos_inf = float('Inf')
neg_inf = float('-Inf')
nan = float('Nan')
