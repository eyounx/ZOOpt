
from zoopt.utils.zoo_global import pos_inf, neg_inf, nan, gl
from zoopt.utils.tool_function import ToolFunction

"""
The class Solution was implemented in this file.

A solution encapsulates a solution vector with attached properties, including dimension information, objective value,
and attachment

Author:
    Yuren Liu
"""


class Solution:

    # value is f(x)
    def __init__(self, x=[], value=nan, resample_value=None, attach=None, post_attach=None, is_in_possible_solution=False):
        self.__x = x
        self.__value = value
        self.__resample_value = resample_value
        self.__attach = attach
        self.__post_attach = post_attach
        self.__is_in_possible_solution = is_in_possible_solution
        return

    @property
    def is_in_possible_solution(self):
        return self.__is_in_possible_solution

    @is_in_possible_solution.setter
    def is_in_possible_solution(self, value):
        self.__is_in_possible_solution = value

    # Deep copy this solution. Note that the attachment is not deeply copied
    def deep_copy(self):
        x = []
        for x_i in self.__x:
            x.append(x_i)
        value = self.__value
        attach = self.__attach
        resample_value = self.__resample_value
        post_attach = self.__post_attach
        return Solution(x, value, resample_value, attach, post_attach, self.is_in_possible_solution)

    # Check if two solutions equal
    def is_equal(self, sol):
        sol_x = sol.get_x()
        sol_value = sol.get_value()
        if sol_value != nan and self.__value != nan:
            if abs(self.__value - sol_value) > gl.precision:
                return False
        if len(self.__x) != len(sol_x):
            return False
        for i in range(len(self.__x)):
            if abs(self.__x[i] - sol_x[i]) > gl.precision:
                return False
        return True

    # Check if exists another solution in sol_set ths same as this one
    def exist_equal(self, sol_set):
        for sol in sol_set:
            if self.is_equal(self, sol):
                return True
        return False

    def set_x_index(self, index, x):
        self.__x[index] = x
        return

    def set_x(self, x):
        self.__x = x
        return

    def set_value(self, value):
        self.__value = value
        return

    def set_attach(self, attach):
        self.__attach = attach
        return

    def set_post_attach(self, attach):
        self.__post_attach = attach
        return

    def set_resample_value(self, resample_value):
        self.__resample_value = resample_value

    def get_resample_value(self):
        return self.__resample_value

    def get_post_attach(self):
        return self.__post_attach

    def get_x_index(self, index):
        return self.__x[index]

    def get_x(self):
        return self.__x

    def get_value(self):
        return self.__value

    def get_attach(self):
        return self.__attach

    def print_solution(self):
        ToolFunction.log('x: ' + repr(self.__x))
        ToolFunction.log('value: ' + repr(self.__value))

    # Deep copy an solution set
    @staticmethod
    def deep_copy_set(sol_set):
        result_set = []
        for sol in sol_set:
            result_set.append(sol.deep_copy())
        return result_set

    # print the value of each solution in an solution set
    @staticmethod
    def print_solution_set(sol_set):
        for sol in sol_set:
            ToolFunction.log('value: %f' % (sol.get_value()))
        return

    # Find the maximum-valued solution from the solution set
    @staticmethod
    def find_maximum(sol_set):
        maxi = neg_inf
        max_index = 0
        for i in range(len(sol_set)):
            if sol_set[i].get_value() > maxi:
                maxi = sol_set[i].get_value()
                max_index = i
        return sol_set[max_index], max_index

    # Find the minimum-valued solution from the solution set
    @staticmethod
    def find_minimum(sol_set):
        mini = pos_inf
        mini_index = 0
        for i in range(len(sol_set)):
            if sol_set[i].get_value() < mini:
                mini = sol_set[i].get_value()
                mini_index = i
        return mini, mini_index
