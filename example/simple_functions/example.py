
#import matplotlib.pyplot as plt  # uncomment this line to plot figures
import time
import numpy as np
from fx import sphere, ackley, setcover, mixed_function
from zoopt import Dimension, Objective, Parameter, Opt, Solution
from zoopt.utils.zoo_global import gl

"""
This file contains some examples about how to use Racos(or SRacos)
optimization algorithm

Author:
    Yuren Liu
"""


# a function to print optimization results
def result_analysis(result, top):
    result.sort()
    top_k = result[0:top]
    mean_r = np.mean(top_k)
    std_r = np.std(top_k)
    print('%f +- %f' % (mean_r, std_r))
    return

# example for minimizing the sphere function
if True:
    t1 = time.clock()
    # repeat of optimization experiments
    repeat = 15
    result = []
    # the random seed for zoopt can be set
    gl.set_seed(12345)
    for i in range(repeat):
        
        # setup optimization problem 
        dim_size = 100  # dimensions
        dim_regs = [[-1, 1]] * dim_size  # dimension range
        dim_tys = [True] * dim_size  # dimension type : real
        dim = Dimension(dim_size, dim_regs, dim_tys)  # form up the dimension object
        objective = Objective(sphere, dim)  # form up the objective function
        
        # setup algorithm parameters
        budget = 1000 # number of calls to the objective function
        parameter = Parameter(budget=budget, sequential=True)  # by default, the algorithm is sequential RACOS
        
        # perform the optimization
        solution = Opt.min(objective, parameter)
        
        # store the optimization result
        print('solved solution is:')
        solution.print_solution()
        result.append(solution.get_value())

        ### to plot the optimization history, uncomment the following codes.
        ### matplotlib is required
        #plt.plot(objective.get_history_bestsofar())
        #plt.savefig("figure.png")
        
    result_analysis(result, 1)
    t2 = time.clock()
    print('time costed %f seconds' % (t2 - t1))

# example for minimizing the ackley function
if True:
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
        budget = 20*dim_size  # number of calls to the objective function
        # by setting autoset=false, the algorithm parameters will not be set by default
        parameter = Parameter(algorithm="racos", budget=budget, autoset=False)
        # so you are allowed to setup algorithm parameters of racos
        parameter.set_train_size(21)
        parameter.set_positive_size(1)
        parameter.set_negative_size(20)
        
        # perform the optimization
        solution = Opt.min(objective, parameter)
        
        # store the optimization result
        print('solved solution is:')
        solution.print_solution()
        result.append(solution.get_value())

        # plt.plot(objective.get_history_bestsofar())
        # plt.savefig("figure.png")
    result_analysis(result, 5)
    t2 = time.clock()
    print('time cost: %f' % (t2 - t1))


# discrete optimization example using minimum set cover instance
if False:
    # repeat of optimization experiments
    # gl.set_seed(12345)
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
        solution.print_solution()

        # store the optimization result
        result.append(solution.get_value())
    result_analysis(result, 10)

# mixed optimization
if False:
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
    result_analysis(result, 5)


