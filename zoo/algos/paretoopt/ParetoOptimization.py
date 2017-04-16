"""
The class RacosOptimization will contains best_solution and optimization algorithm(Racos or SRacos)

Author:
    Yu-Ren Liu

"""

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

from zoo.algos.paretoopt.paretoopt import ParetoOpt


class ParetoOptimization:

    def __init__(self):
        self._best_solution = None
        self._algorithm = None

    def clear(self):
        self._best_solution = None
        self._algorithm = None

    # General optimization function, it will choose concrete optimization algorithm
    def opt(self, objective, parameter):
        self.clear()
        self._algorithm = ParetoOpt()
        paretoParameter = parameter.get_paretoopt_parameters()
        self._best_solution = self._algorithm.opt(paretoParameter[0], paretoParameter[1], paretoParameter[2])
        return self._best_solution

    def get_best_sol(self):
        return self._best_solution

