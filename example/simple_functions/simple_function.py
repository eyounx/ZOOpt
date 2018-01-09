"""
Objective functions can be implemented in this file.

Author:
    Yu-Ren Liu
"""

from random import Random
from zoopt.dimension import Dimension
import numpy as np


class SetCover:
    """
    set cover problem for discrete optimization
    this problem has some extra initialization tasks, thus we define this problem as a class
    """
    __weight = None
    __subset = None

    def __init__(self):
        self.__weight = [0.8356, 0.5495, 0.4444, 0.7269, 0.9960, 0.6633, 0.5062, 0.8429, 0.1293, 0.7355,
                         0.7979, 0.2814, 0.7962, 0.1754, 0.0267, 0.9862, 0.1786, 0.5884, 0.6289, 0.3008]
        self.__subset = []
        self.__subset.append([0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0])
        self.__subset.append([0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0])
        self.__subset.append([1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0])
        self.__subset.append([0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0])
        self.__subset.append([1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1])
        self.__subset.append([0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0])
        self.__subset.append([0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0])
        self.__subset.append([0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0])
        self.__subset.append([0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0])
        self.__subset.append([0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1])
        self.__subset.append([0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0])
        self.__subset.append([0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1])
        self.__subset.append([1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1])
        self.__subset.append([1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1])
        self.__subset.append([0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1])
        self.__subset.append([1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0])
        self.__subset.append([1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1])
        self.__subset.append([0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1])
        self.__subset.append([0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0])
        self.__subset.append([0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1])

    def fx(self, solution):
        """
        Objective function.

        :param solution: a Solution object
        :return: the value of f(x)
        """
        x = solution.get_x()
        allweight = 0
        countw = 0
        for i in range(len(self.__weight)):
            allweight += self.__weight[i]

        dims = []
        for i in range(len(self.__subset[0])):
            dims.append(False)

        for i in range(len(self.__subset)):
            if x[i] == 1:
                countw += self.__weight[i]
                for j in range(len(self.__subset[i])):
                    if self.__subset[i][j] == 1:
                        dims[j] = True
        full = True
        for i in range(len(dims)):
            if dims[i] is False:
                full = False

        if full is False:
            countw += allweight

        return countw

    @property
    def dim(self):
        """
        Dimension of set cover problem.
        :return: Dimension instance
        """
        dim_size = 20
        dim_regs = [[0, 1]] * dim_size
        dim_tys = [False] * dim_size
        return Dimension(dim_size, dim_regs, dim_tys)


def sphere(solution):
    """
    Sphere function for continuous optimization
    """
    x = solution.get_x()
    value = sum([(i-0.2)*(i-0.2) for i in x])
    return value


def sphere_mixed(solution):
    """
    Sphere function for mixed optimization
    """
    x = solution.get_x()
    value = sum([i*i for i in x])
    return value


def sphere_discrete_order(solution):
    """
    Sphere function for integer continuous optimization
    """
    a = 0
    rd = Random()
    x = solution.get_x()
    value = sum([(i-2)*(i-2) for i in x])
    return value


def ackley(solution):
    """
    Ackley function for continuous optimization
    """
    x = solution.get_x()
    bias = 0.2
    ave_seq = sum([(i - bias) * (i - bias) for i in x]) / len(x)
    ave_cos = sum([np.cos(2.0*np.pi*(i-bias)) for i in x]) / len(x)
    value = -20 * np.exp(-0.2 * np.sqrt(ave_seq)) - np.exp(ave_cos) + 20.0 + np.e
    return value


def ackley_noise_creator(mu, sigma):
    """
    Ackley function under noise
    """
    return lambda solution: ackley(solution) + np.random.normal(mu, sigma, 1)






