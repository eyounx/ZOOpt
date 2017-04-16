""""
The class solution was implemented in this file.

A solution encapsulates a solution vector with attached properties, including dimension information, objective value,
and attachment

Author:
    Yuren Liu

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 as published by the Free Software Foundation; either version 2
 of the License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

 Copyright (C) 2017 Nanjing University, Nanjing, China
"""
from zoo.utils.my_global import pos_inf, neg_inf, nan


class Solution:

    def __init__(self, x=[], value=nan, attach=None):
        self.__x = x
        self.__value = value
        self.__attach = attach
        return

    # Deep copy this solution. Note that the attachment is not deeply copied
    def deep_copy(self):
        x = []
        for x_i in self.__x:
            x.append(x_i)
        value = self.__value
        attach = self.__attach
        return Solution(x, value, attach)

    # Check if two solutions equal
    def is_equal(self, sol, precision=1e-17):
        sol_x = sol.get_x()
        sol_value = sol.get_value()
        if abs(self.__value - sol_value) > precision:
            return False
        if len(self.__x) != len(sol_x):
            return False
        for i in range(len(self.__x)):
            if abs(self.__x[i] - sol_x[i]) > precision:
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

    def get_x_index(self, index):
        return self.__x[index]

    def get_x(self):
        return self.__x

    def get_value(self):
        return self.__value

    def get_attach(self):
        return self.__attach

    def print_solution(self):
        print 'x is: ' + repr(self.__x)
        print 'value is ' + repr(self.__value)

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
            print 'value is %f' % (sol.get_value())
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



