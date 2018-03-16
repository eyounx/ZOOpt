"""
This module contains the class Objective

Author:
    Yu-Ren Liu, Xiong-Hui Chen
"""

from zoopt.solution import Solution
from zoopt.utils.zoo_global import pos_inf
from zoopt.utils.tool_function import ToolFunction
import numpy as np


class Objective:
    """
    This class represents the objective function and its associated variables
    """
    def __init__(self, func=None, dim=None, constraint=None, resample_func=None):
        """
        Initialization.

        :param func: objective function defined by the user
        :param dim: a Dimension object, which describes the search space.
        :param constraint: constraint function for POSS
        :param resample_func: resample function for SSRacos
        :param reducedim: whether to use sequential random embedding
        """
        self.__func = func
        self.__dim = dim
        # the function for inheriting solution attachment
        self.__inherit = self.default_inherit
        self.__post_inherit = self.default_post_inherit
        # the constraint function
        self.__constraint = constraint
        # the history of optimization
        self.__history = []

        self.__resample_times = 1
        self.__resample_func = self.resample_func if resample_func is None else resample_func
        self.__balance_rate = 1
        # for sequential random embedding
        self.__reducedim = False
        self.__A = None
        self.__last_x = None

    def parameter_set(self, parameter):
        """
        Use a Parameter object to set attributes in Objective object.

        :param parameter: a Parameter object
        :return: no return
        """
        if parameter.get_noise_handling() is True and parameter.get_suppression() is True:
            self.__balance_rate = parameter.get_balance_rate()
        if parameter.get_noise_handling() is True and parameter.get_resampling() is True:
            self.__resample_times = parameter.get_resample_times()
        if parameter.get_high_dim_handling() is True and parameter.get_reducedim() is True:
            self.__reducedim = True

    def construct_solution(self, x, parent=None):
        """
        Construct a solution from x

        :param x: a list
        :param parent: the attached structure
        :return: solution
        """
        new_solution = Solution()
        new_solution.set_x(x)
        new_solution.set_attach(self.__inherit(parent))
        return new_solution

    def eval(self, solution):
        """
        Use the objective function to evaluate a solution.

        :param solution:
        :return: value of fx(evaluation result) will be returned
        """
        res = []
        for i in range(self.__resample_times):
            if self.__reducedim is False:
                val = self.__func(solution)
            else:
                x = solution.get_x()
                x_origin = x[0] * np.array(self.__last_x.get_x()) + np.dot(self.__A, np.array(x[1:]))
                val = self.__func(Solution(x=x_origin))
            res.append(val)
            self.__history.append(val)
        value = sum(res) / float(len(res))
        solution.set_value(value)
        solution.set_post_attach(self.__post_inherit())
        return value

    def resample(self, solution, repeat_times):
        """
        Resample function for value suppression.

        :param solution: a Solution object
        :param repeat_times: repeat times
        :return: repeat times
        """
        if solution.get_resample_value() is None:
            solution.set_resample_value(self.__resample_func(solution, repeat_times))
            solution.set_value((1 - self.__balance_rate) * solution.get_value() +
                               self.__balance_rate * solution.get_resample_value())
            solution.set_post_attach(self.__post_inherit())
            return repeat_times
        else:
            return 0

    def resample_func(self, solution, iteration_num):
        result = []
        for i in range(iteration_num):
            result.append(self.eval(solution))
        return sum(result) * 1.0 / len(result)

    def eval_constraint(self, solution):
        solution.set_value(
            [self.eval(solution), self.__constraint(solution)])
        solution.set_post_attach(self.__post_inherit())

    def set_func(self, func):
        """
        Set the objective function
        :param func: the objective function
        :return: no return value
        """
        self.__func = func

    def get_func(self):
        return self.__func

    def set_dim(self, dim):
        self.__dim = dim

    def get_dim(self):
        return self.__dim

    def set_inherit_func(self, inherit_func):
        self.__inherit = inherit_func

    def set_post_inherit_func(self, inherit_func):
        self.__post_inherit = inherit_func

    def get_post_inherit_func(self):
        return self.__post_inherit

    def get_inherit_func(self):
        return self.__inherit

    def set_constraint(self, constraint):
        self.__constraint = constraint
        return

    def get_constraint(self):
        return self.__constraint

    def set_history(self, history):
        self.__history = history

    def get_history(self):
        return self.__history

    def get_history_bestsofar(self):
        """
        Get the best-so-far history.
        """
        history_bestsofar = []
        bestsofar = pos_inf
        for i in range(len(self.__history)):
            if self.__history[i] < bestsofar:
                bestsofar = self.__history[i]
            history_bestsofar.append(bestsofar)
        return history_bestsofar

    def get_reducedim(self):
        return self.__reducedim

    def get_last_x(self):
        return self.__last_x

    def get_A(self):
        return self.__A

    def set_A(self, A):
        self.__A = A

    def set_last_x(self, x):
        self.__last_x = x

    def clean_history(self):
        """
        clean the optimization history
        """
        self.__history = []

    @staticmethod
    def default_inherit(parent=None):
        """
        Default inherited function.

        :param parent: the parent structure
        :return: None
        """
        return None

    @staticmethod
    def default_post_inherit(parent=None):
        """
        Default post inherited function.

        :param parent: the parent structure
        :return: None
        """
        return None
