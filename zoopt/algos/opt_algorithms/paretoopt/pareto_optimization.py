
"""
The class ParetoOptimization is a wrapper of Pareto optimization methods, even though currently there is only the canonical Pareto optimization method

Author:
    Yu-Ren Liu

"""

from zoopt.algos.noise_handling.ponss import PONSS
from zoopt.algos.opt_algorithms.paretoopt.paretoopt import ParetoOpt


class ParetoOptimization:
    """
    Pareto optimization.
    """

    def __init__(self):
        self.__best_solution = None
        self.__algorithm = None

    def clear(self):
        self.__best_solution = None
        self.__algorithm = None

    def opt(self, objective, parameter):
        """
        The optimization procedure.

        :param objective: an Objective object
        :param parameter: a Parameter object
        :return: the best solution
        """
        self.clear()
        if parameter.get_noise_handling() is True and parameter.get_ponss() is True:
            self.__algorithm = PONSS()
        else:
            self.__algorithm = ParetoOpt()
        self.__best_solution = self.__algorithm.opt(objective, parameter)
        return self.__best_solution

    def get_best_sol(self):
        return self.__best_solution
