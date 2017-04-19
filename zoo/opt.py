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
from zoo.algos.paretoopt.ParetoOptimization import ParetoOptimization
from zoo.algos.racos.racos_optimization import RacosOptimization
from zoo.utils.zoo_global import gl
from zoo.utils.tool_function import ToolFunction

"""
The class Opt is the main entrance of using zoo: Opt.min(objective, parameter)

Author:
    Yuren Liu
"""


class Opt:
    def __init__(self):
        return

    @staticmethod
    def min(objective, parameter):
        Opt.set_global(parameter)
        constraint = objective.get_constraint()
        algorithm = parameter.get_algorithm()
        if algorithm:
            algorithm = algorithm.lower()
        result = None
        if constraint is not None and ((algorithm is None) or (algorithm == "poss")):
            optimizer = ParetoOptimization()
            result = optimizer.opt(objective, parameter)
        elif constraint is None and ((algorithm is None) or (algorithm == "racos")):
            optimizer = RacosOptimization()
            result = optimizer.opt(objective, parameter)
        else:
            ToolFunction.log("opt.py: No proper algorithm find for %s" % algorithm)
        return result

    @staticmethod
    def set_global(parameter):
        precision = parameter.get_precision()
        if precision:
            gl.set_precision(precision)
