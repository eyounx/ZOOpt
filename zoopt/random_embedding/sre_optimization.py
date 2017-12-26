"""
The class Dimension was implemented in this file.

This class describes dimension messages.

Author:
    Yuren Liu
"""

from zoopt.solution import Solution
from zoopt.dimension import Dimension
import numpy as np


class SequentialRandomEmbedding:
    def __init__(self, objective, parameter, optimizer):
        self.__objective = objective
        self.__parameter = parameter
        self.__optimizer = optimizer

    def opt(self):
        dim = self.__objective.get_dim()
        self.__objective.set_last_x(Solution(x=[0]))
        res = []
        for i in range(self.__parameter.get_num_sre()):
            self.__objective.set_A(np.sqrt(self.__parameter.get_variance_A()) *
                                   np.random.randn((dim.get_size(), self.__parameter.get_low_dimension().get_size())))
            new_dim = Dimension.merge_dim(self.__parameter.get_withdraw_alpha(), self.__parameter.get_low_dimension())
            self.__objective.set_dim(new_dim)
            result = self.__optimizer.opt(self.__objective, self.__parameter)
            x = result.get_x()
            x_origin = x[0] * self.__objective.get_last_x() + np.multiply(self.__objective.get_A(), np.array(x[1:]))
            res.append(Solution(x=x_origin, value=result.get_value()))
        best_sol = res[0]
        for i in range(len(res)):
            if res[i].get_value() < best_sol.get_value():
                best_sol = res[i]
        return best_sol
