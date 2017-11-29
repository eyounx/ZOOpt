from zoopt.algos.racos.ssracos import SSRacos
from zoopt.algos.racos.ssracos2 import SSRacos2

from zoopt.algos.racos.sracos import SRacos
from zoopt.algos.racos.racos import Racos

"""
The class RacosOptimization will contains best_solution and optimization algorithm(Racos or SRacos)

Author:
    Yuren Liu
"""


class RacosOptimization:

    def __init__(self):
        self.__best_solution = None
        self.__algorithm = None

    def clear(self):
        self.__best_solution = None
        self.__algorithm = None

    # General optimization function, it will choose optimization algorithm according to parameter.get_sequential()
    # Default replace strategy is 'WR'
    # If user hasn't define uncertain_bits in parameter, set_ub() will set uncertain_bits automatically according to dim
    # in objective
    def opt(self, objective, parameter, strategy='WR'):
        self.clear()
        ub = parameter.get_uncertain_bits()
        if ub is None:
            ub = self.set_ub(objective)
        if parameter.get_sequential():
            if not parameter.get_suppressioin():
                self.__algorithm = SRacos()
                self.__best_solution = self.__algorithm.opt(
                    objective, parameter, strategy, ub)
            else:

                self.__algorithm = SSRacos2()
                # self.__algorithm = SSRacos2()
                self.__best_solution = self.__algorithm.opt(
                    objective, parameter, strategy, ub)
        else:
            self.__algorithm = Racos()
            self.__best_solution = self.__algorithm.opt(
                objective, parameter, ub)
        return self.__best_solution

    def get_best_sol(self):
        return self.__best_solution

    @staticmethod
    # Set uncertain_bits
    def set_ub(objective):
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
