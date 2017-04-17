"""
The class RacosOptimization will contains best_solution and optimization algorithm(Racos or SRacos)

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
from zoo.algos.racos.sracos import SRacos
from zoo.algos.racos.racos import Racos
from zoo.objective import Objective


class RacosOptimization:

    def __init__(self):
        self.__best_solution = None
        self.__algorithm = None

    def clear(self):
        self.__best_solution = None
        self.__algorithm = None

    # General optimization function, it will choose optimization algorithm according to parameter.get_sequential()
    # Default replace strategy is 'WR'
    def opt(self, objective, parameter, strategy='WR'):
        self.clear()
        ub = parameter.get_uncertain_bits()
        if ub is None:
            ub = Objective.set_ub(objective)
        if parameter.get_sequential() is True:
            self.__algorithm = SRacos()
            self.__best_solution = self.__algorithm.opt(objective, parameter, strategy, ub)
        else :
            self.__algorithm = Racos()
            self.__best_solution = self.__algorithm.opt(objective, parameter, ub)
        return self.__best_solution

    def get_best_sol(self):
        return self.__best_solution
