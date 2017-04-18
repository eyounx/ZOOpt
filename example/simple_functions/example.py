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
# import matplotlib.pyplot as plt # uncomment this line to plot figures
import time
import numpy as np
from fx import sphere, ackley, setcover, mixed_function
from zoo.dimension import Dimension
from zoo.objective import Objective
from zoo.parameter import Parameter
from zoo.opt import Opt
from zoo.utils.zoo_global import gl

"""
This file contains some examples about how to use Racos(or SRacos)
optimization algorithm

Author:
    Yuren Liu
"""

### a function to print optimization results
def result_analysis(result, top):
    result.sort()
    top_k = result[0:top]
    mean_r = np.mean(top_k)
    std_r = np.std(top_k)
    print mean_r, '#', std_r
    return

### example for minimizing the sphere function
if False:
    t1 = time.clock()
    # repeat of optimization experiments
    repeat = 5
    result = []
    gl.set_seed(12345)
    for i in range(repeat):
        
        # setup optimization problem 
        dim_size = 100  # dimensions
        dim_regs = [[-1, 1]] * dim_size  # dimension range
        dim_tys = [True] * dim_size  # dimension type : real
        dim = Dimension(dim_size, dim_regs, dim_tys)  # form up the dimension object
        objective = Objective(sphere, dim)  # form up the objective function
        
        # setup algorithm parameters
        budget = 100*dim_size # number of calls to the objective function
        parameter = Parameter(budget=budget)  # by default, the algorithm is sequential RACOS
        
        # perform the optimization
        solution = Opt.min(objective, parameter)
        
        # store the optimization result
        print 'Best solution is:'
        solution.print_solution()
        result.append(solution.get_value())

        ### to plot the optimization history, uncomment the following codes.
        ### matplotlib is required
        # plt.plot(objective.get_history_bestsofar())
        # plt.savefig("figure.png")
        
    result_analysis(result, 5)
    t2 = time.clock()
    print 'time costed %f seconds' % (t2 - t1)

### example for minimizing the ackley function
if True:
    # the random seed for zoo can be set
    gl.set_seed(12345)
    t1 = time.clock()
    # repeat of optimization experiments
    repeat = 15
    result = []
    for i in range(repeat):

        # setup optimization problem
        dim_size = 100  # dimensions
        dim_regs = [[-1, 1]] * dim_size  # dimension range
        dim_tys = [True] * dim_size  # dimension type : real
        dim = Dimension(dim_size, dim_regs, dim_tys)  # form up the dimension object
        objective = Objective(ackley, dim)  # form up the objective function
        budget = 100*dim_size  # number of calls to the objective function
        # by setting autoset=false, the algorithm parameters will not be set by default
        parameter = Parameter(algorithm="racos", budget=budget, autoset=False)
        # so you are allowed to setup algorithm parameters of racos
        parameter.set_train_size(21)
        parameter.set_positive_size(1)
        parameter.set_negative_size(20)
        
        # perform the optimization
        solution = Opt.min(objective, parameter)
        
        # store the optimization result
        print 'Best solution is:'
        solution.print_solution()
        result.append(solution.get_value())
        
    result_analysis(result, 100)
    t2 = time.clock()
    print 'time is %f' % (t2 - t1)


### discrete optimization example using minimum set cover instance
if True:
    # repeat of optimization experiments
    gl.set_seed(12345)
    repeat = 10
    result = []
    for i in range(repeat):

        # setup problem
        problem = setcover()  # instantialize a set cover instance
        dim = problem.dim  # the dim is prepared by the class
        objective = Objective(problem.fx, dim)  # form up the objective function
        budget = 100 * dim.get_size()  # number of calls to the objective function
        parameter = Parameter(budget=budget, autoset=False)
        parameter.set_train_size(6)
        parameter.set_positive_size(1)
        parameter.set_negative_size(5)

        # perform the optimization
        solution = Opt.min(objective, parameter)

        # store the optimization result
        print 'Best solution is:'
        solution.print_solution()
        result.append(solution.get_value())
    result_analysis(result, 100)

# mixed optimization
if True:
    repeat = 15
    result = []
    gl.set_seed(12345)
    for j in range(repeat):
        dim_size = 10
        dim_regs = []
        dim_tys = []
        # In this example, dimension is mixed. If dimension index is odd, this dimension if discrete, Otherwise, this
        # dimension is continuous.
        for i in range(dim_size):
            if i%2 == 0:
                dim_regs.append([0, 1])
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
