"""
This module contains the class RacosOptimization, which will choose the optimization algorithm and get the best solution.

Author:
    Yu-Ren Liu
"""

from zoopt.algos.noise_handling.ssracos import SSRacos
from zoopt.algos.opt_algorithms.racos.racos import Racos
from zoopt.algos.opt_algorithms.racos.sracos import SRacos


class RacosOptimization:
    """
    This class will choose the optimization algorithm and get the best solution.
    """

    def __init__(self):
        """
        Initialization.
        """
        self.__best_solution = None
        self.__algorithm = None

    def clear(self):
        """
        Clear the instance.

        :return: no return value
        """
        self.__best_solution = None
        self.__algorithm = None

    def opt(self, objective, parameter, strategy='WR'):
        """
        This function will choose optimization algorithm and use it to optimize.

        :param objective: a Objective object
        :param parameter: a Parameter object
        :param strategy: replace strategy, used by SRacos and SSRacos
        :return: the best solution
        """

        self.clear()
        ub = parameter.get_uncertain_bits()
        if ub is None:
            ub = self.choose_ub(objective)
        if parameter.get_sequential():
            if parameter.get_noise_handling() is True and parameter.get_suppression() is True:
                self.__algorithm = SSRacos()
            else:
                self.__algorithm = SRacos()
            self.__best_solution = self.__algorithm.opt(
                objective, parameter, strategy, ub)
        else:
            self.__algorithm = Racos()
            self.__best_solution = self.__algorithm.opt(
                objective, parameter, ub)
        return self.__best_solution

    @staticmethod
    def choose_ub(objective):
        """
        Choose uncertain_bits according to the dimension size automatically.

        :param objective: an Objective object
        :return: uncertain bits
        """
        dim = objective.get_dim()
        dim_size = dim.get_size()
        is_discrete = dim.is_discrete()
        if is_discrete is False:
            if dim_size <= 100:
                ub = 1
            elif dim_size <= 1000:
                ub = 2
            else:
                ub = 3
        else:
            if dim_size <= 10:
                ub = 1
            elif dim_size <= 50:
                ub = 2
            elif dim_size <= 100:
                ub = 3
            elif dim_size <= 1000:
                ub = 4
            else:
                ub = 5
        return ub

    def get_best_sol(self):
        return self.__best_solution
