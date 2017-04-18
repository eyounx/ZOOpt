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

"""
The class Objective was implemented in this file.
This class contains a func and  a dim

Author:
    Yuren Liu
"""
from zoo.solution import Solution


class Objective:
    def __init__(self, func=None, dim=None, constraint=None):
        # Objective function defined by the user
        self.__func = func
        # Number of dimensions, dimension bounds are in the dim object
        self.__dim = dim
        # the function for inheriting solution attachment
        self.__inherit = self.default_inherit
        self._constraint = constraint

    # Construct a solution from x
    def construct_solution(self, x, parent=None):
        new_solution = Solution()
        new_solution.set_x(x)
        new_solution.set_attach(self.__inherit(parent))
        new_solution.set_value(self.__func(new_solution))
        return new_solution

    def set_func(self, func):
        self.__func = func

    def get_func(self):
        return self.__func

    def set_dim(self, dim):
        self.__dim = dim

    def get_dim(self):
        return self.__dim

    def set_inherit_func(self, inherit_func):
        self.__inherit=inherit_func

    def get_inherit_func(self):
        return self.__inherit

    def set_constraint(self, constraint):
        self._constraint = constraint
        return

    def get_constraint(self):
        return self._constraint

    @staticmethod
    def default_inherit(parent=None):
        return None
