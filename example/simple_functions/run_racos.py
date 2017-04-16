"""
This file contains some examples about how to use Racos(or SRacos)
optimization algorithm

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
import time
import numpy as np

from example.simple_functions.fx import sphere, ackley, set_cover, mixed_function
from zoo.dimension import Dimension
from zoo.objective import Objective
from zoo.parameter import Parameter
from zoo.opt import Opt
from zoo.utils.my_global import gl


def result_analysis(result, top):
    result.sort()
    top_k = result[0:top]
    mean_r = np.mean(top_k)
    std_r = np.std(top_k)
    print mean_r, '#', std_r
    return


# Sphere
if True:
    t1 = time.clock()
    repeat = 15
    result = []
    # Set random seed in sample
    for i in range(repeat):
        dim_size = 100
        dim_regs = [[-1, 1]] * dim_size
        dim_tys = [True] * dim_size
        dim = Dimension(dim_size, dim_regs, dim_tys)
        # objective means objective function
        objective = Objective(sphere, dim)
        budget = 20 * 2000
        parameter = Parameter(algorithm="racos", budget=budget)
        solution = Opt.min(objective, parameter)
        print 'Best solution is:'
        solution.print_solution()
        result.append(solution.get_value())
    result_analysis(result, 5)
    t2 = time.clock()
    print 'time is %f' % (t2 - t1)

# Ackley
if True:
    t1 = time.clock()
    repeat = 15
    result = []
    gl.set_seed(12345)
    for i in range(repeat):
        dim_size = 10
        dim_regs = [[-1, 1]] * dim_size
        dim_tys = [True] * dim_size
        dim = Dimension(dim_size, dim_regs, dim_tys)
        objective = Objective(ackley, dim)
        budget = 5000
        parameter = Parameter(algorithm="racos", budget=budget, autoset=False)
        parameter.set_train_size(21)
        parameter.set_positive_size(1)
        parameter.set_negative_size(20)
        solution = Opt.min(objective, parameter)
        print 'Best solution is:'
        solution.print_solution()
        result.append(solution.get_value())
    result_analysis(result, 100)
    t2 = time.clock()
    print 'time is %f' % (t2 - t1)

# discrete optimization
if True:
    # dimension setting
    repeat = 10
    result = []
    for i in range(repeat):
        dim_size = 20
        dim_regs = [[-1, 1]] * dim_size
        dim_tys = [True] * dim_size
        dim = Dimension(dim_size, dim_regs, dim_tys)
        objective = Objective(set_cover, dim)
        budget = 2000
        parameter = Parameter(budget=budget, autoset=False)
        parameter.set_train_size(6)
        parameter.set_positive_size(1)
        parameter.set_negative_size(5)
        solution = Opt.min(objective, parameter)
        solution.print_solution()
        result.append(solution.get_value())
    result_analysis(result, 100)

# mixed optimization
if False:
    repeat = 15
    result = []
    for j in range(repeat):
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
        objective = Objective(mixed_function, dim)
        budget = 2000
        parameter = Parameter(budget=budget, autoset=True)
        solution = Opt.min(objective, parameter)
        solution.print_solution()
        result.append(solution.get_value())
    result_analysis(result, 15)
