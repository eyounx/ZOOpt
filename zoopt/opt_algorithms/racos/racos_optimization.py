"""
This module contains the class RacosOptimization, which will choose the optimization algorithm and get the best solution.

Author:
    Yu-Ren Liu
"""

from zoopt.opt_algorithms.racos.racos import Racos
from zoopt.opt_algorithms.racos.sracos import SRacos
from zoopt.noise_handling.ssracos import SSRacos


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

        :return: no return
        """
        self.__best_solution = None
        self.__algorithm = None

    def opt(self, objective, parameter, strategy='WR'):
        """
        This function will choose optimization algorithm and use it to optimize.

        :param objective: objective function
        :param parameter: parameter
        :param strategy: replace strategy, used by SRacos and SSRacos
        :return:
        """

        self.clear()
        ub = parameter.get_uncertain_bits()
        if ub is None:
            ub = self.choose_ub(objective)
        if parameter.get_sequential():
            if not parameter.get_suppressioin():
                self.__algorithm = SRacos()
                self.__best_solution = self.__algorithm.opt(
                    objective, parameter, strategy, ub)
            else:

                self.__algorithm = SSRacos()
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
        Choose uncertain_bits according to dimension size automatically.

        :param objective: objective function
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

