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
  LAMDA, http://lamda.nju.edu.cn
"""
from zoo.algos.racos.sracos import SRacos
from zoo.algos.racos.racos import Racos

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
        if parameter.get_sequential() is True:
            self.__algorithm = SRacos()
            self.__best_solution = self.__algorithm.opt(objective, parameter, strategy, ub)
        else :
            self.__algorithm = Racos()
            self.__best_solution = self.__algorithm.opt(objective, parameter, ub)
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
