"""
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
from zoo.solution import Solution
from zoo.utils.zoo_global import pos_inf

"""
The class Objective represents the objective function and its associated variables

Author:
    Yuren Liu
"""


class Objective:
    def __init__(self, func=None, dim=None, constraint=None):
        # Objective function defined by the user
        self.__func = func
        # Number of dimensions, dimension bounds are in the dim object
        self.__dim = dim
        # the function for inheriting solution attachment
        self.__inherit = self.default_inherit
        # the constraint function
        self._constraint = constraint
        # the history of optimization
        self.__history = []

    # Construct a solution from x
    def construct_solution(self, x, parent=None):
        new_solution = Solution()
        new_solution.set_x(x)
        new_solution.set_attach(self.__inherit(parent))
        # new_solution.set_value(self.__func(new_solution)) # evaluation should be invoked explicitly
        return new_solution

    # evaluate the objective function of a solution
    def eval(self, solution):
        solution.set_value(self.__func(solution))
        self.__history.append(solution.get_value())

    # set the optimization function
    def set_func(self, func):
        self.__func = func

    # get the optimization function
    def get_func(self):
        return self.__func

    # set the dimension object
    def set_dim(self, dim):
        self.__dim = dim

    # get the dimension object
    def get_dim(self):
        return self.__dim

    # set the attachment inheritance function
    def set_inherit_func(self, inherit_func):
        self.__inherit=inherit_func

    # get the attachment inheritance function
    def get_inherit_func(self):
        return self.__inherit

    # set the constraint function
    def set_constraint(self, constraint):
        self._constraint = constraint
        return

    # return the constraint function
    def get_constraint(self):
        return self._constraint

    # get the optimization history
    def get_history(self):
        return self.__history

    # get the best-so-far history
    def get_history_bestsofar(self):
        history_bestsofar = []
        bestsofar = pos_inf
        for i in range(len(self.__history)):
            if self.__history[i] < bestsofar:
                bestsofar = self.__history[i]
            history_bestsofar.append(bestsofar)
        return history_bestsofar

    # clean the optimization history
    def clean_history(self):
        self.__history=[]

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

    @staticmethod
    def default_inherit(parent=None):
        return None
