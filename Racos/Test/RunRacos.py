"""
This file contains some examples about how to use Racos(or SRacos)
optimization algorithm

Author:
    Yu-Ren Liu

Time:
    2017.1.20
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

 Copyright (C) 2015 Nanjing University, Nanjing, China
"""

import time

import numpy as np

from Racos.Method.Racos import Dimension
from Racos.Method.Racos import Objective
from Racos.Method.Racos import Parameter
from Racos.Method.RacosOptimization import RacosOptimization
from Racos.ObjectiveFunction.ObjectFunction import Sphere, Arkley, SetCover, MixedFunction


def result_analysis(result, top):
    result.sort()
    top_k = result[0:top]
    mean_r = np.mean(top_k)
    std_r = np.std(top_k)
    print mean_r, '#', std_r
    return


# Sphere
if False:
    t1 = time.clock()
    repeat = 15
    result = []
    for i in range(repeat):
        dim_size = 100
        dim_regs = []
        dim_tys = []
        for i in range(dim_size):
            dim_regs.append([0, 1])
            dim_tys.append(True)

        dim = Dimension(dim_size, dim_regs, dim_tys)
        objective = Objective(Sphere, dim)
        budget = 20 * dim_size
        parameter = Parameter(objective, budget)
        racos = RacosOptimization()
        print 'Best solution is:'
        ins = racos.opt(parameter, strategy='WR')
        ins.print_instance()
        result.append(ins.get_value())
    result_analysis(result, 5)
    t2 = time.clock()
    print 'time is %f' % (t2 - t1)

# Arkley
if False:
    t1 = time.clock()
    repeat = 15
    result = []
    for i in range(repeat):
        dim_size = 10
        dim_regs = []
        dim_tys = []
        for i in range(dim_size):
            dim_regs.append([-1, 1])
            dim_tys.append(True)
        dim = Dimension(dim_size, dim_regs, dim_tys)
        objective = Objective(Arkley, dim)
        budget = 500
        parameter = Parameter(objective, budget, autoset=False)
        parameter.set_train_size(21)
        parameter.set_positive_size(1)
        parameter.set_negative_size(20)
        racos = RacosOptimization()
        ins = racos.opt(parameter, 'SRacos')
        ins.print_instance()
        result.append(ins.get_value())
    result_analysis(result, 100)
    t2 = time.clock()
    print 'time is %f' % (t2 - t1)

# discrete optimization
if False:
    # dimension setting
    repeat = 100
    result = []
    for i in range(repeat):
        dim_size = 20
        dim_regs = []
        dim_tys = []
        for i in range(dim_size):
            dim_regs.append([0, 1])
            dim_tys.append(False)
        dim = Dimension(dim_size, dim_regs, dim_tys)
        objective = Objective(SetCover, dim)
        budget = 2000
        parameter = Parameter(objective, budget, autoset=False)
        parameter.set_train_size(6)
        parameter.set_positive_size(1)
        parameter.set_negative_size(5)
        racos = RacosOptimization()
        ins = racos.opt(parameter, 'SRacos')
        ins.print_instance()
        result.append(ins.get_value())
    result_analysis(result, 100)

# mixed optimization
if True:
    repeat = 15
    result = []
    for i in range(repeat):
        dim_size = 10
        dim_regs = []
        dim_tys = []
        for i in range(dim_size):
            if i%2 == 0:
                dim_regs.append([-1, 1])
                dim_tys.append(True)
            else:
                dim_regs.append([0, 100])
                dim_tys.append(False)
        dim = Dimension(dim_size, dim_regs, dim_tys)
        objective = Objective(MixedFunction, dim)
        budget = 2000
        parameter = Parameter(objective, budget, autoset=True)
        # parameter.set_train_size(6)
        # parameter.set_positive_size(1)
        # parameter.set_negative_size(5)
        racos = RacosOptimization()
        ins = racos.opt(parameter, 'Racos')
        ins.print_instance()
        result.append(ins.get_value())
    result_analysis(result, 15)