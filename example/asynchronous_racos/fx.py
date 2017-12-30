"""
This file contains objective functions for asynchronous racos.

Author:
    Yu-Ren Liu
"""

from random import Random
import numpy as np



def sphere(solution):
    """
    Sphere function for continuous optimization

    :param solution: a data structure containing x and fx
    :return: value of fx
    """
    a = 0
    rd = Random()
    for i in range(100000):
        a += rd.uniform(0, 1)
    x = solution.get_x()
    value = sum([(i-0.2)*(i-0.2) for i in x])
    return value


def ackley(solution):
    """
        Ackley function for continuous optimization

        :param solution: a data structure containing x and fx
        :return: value of fx
    """
    # a = 0
    # rd = Random()
    # for i in range(100000):
    #     a += rd.uniform(0, 1)
    x = solution.get_x()
    bias = 0.2
    ave_seq = sum([(i - bias) * (i - bias) for i in x]) / len(x)
    ave_cos = sum([np.cos(2.0 * np.pi * (i - bias)) for i in x]) / len(x)
    value = -20 * np.exp(-0.2 * np.sqrt(ave_seq)) - np.exp(ave_cos) + 20.0 + np.e
    return value
