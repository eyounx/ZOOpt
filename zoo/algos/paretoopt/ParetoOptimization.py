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
from zoo.algos.paretoopt.paretoopt import ParetoOpt

"""
The class ParetoOptimization is a wrapper of Pareto optimization methods, even though currently there is only the canonical Pareto optimization method

Author:
    Yu-Ren Liu

"""

class ParetoOptimization:

    def __init__(self):
        self.__best_solution = None
        self.__algorithm = None

    def clear(self):
        self.__best_solution = None
        self.__algorithm = None

    # General optimization function, it will choose concrete optimization algorithm
    def opt(self, objective, parameter):
        self.clear()
        self.__algorithm = ParetoOpt()
        self.__best_solution = self.__algorithm.opt(objective, parameter)
        return self.__best_solution

    def get_best_sol(self):
        return self.__best_solution

