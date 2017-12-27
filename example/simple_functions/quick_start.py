import matplotlib.pyplot as plt  # uncomment this line to plot figures
import time
import numpy as np
from fx import sphere, ackley, setcover, ackley_noise_creator
from zoopt import Dimension, Objective, Parameter, Opt, Solution
from zoopt.utils.zoo_global import gl

"""
This file contains some examples about how to use Racos(or SRacos)
optimization algorithm

Author:
    Yuren Liu, Xionghui Chen
"""


# a function to print optimization results
def result_analysis(result, top):
    limit = top if top < len(result) else len(result)
    result.sort()
    top_k = result[0:limit]
    mean_r = np.mean(top_k)
    std_r = np.std(top_k)
    print('%f +- %f' % (mean_r, std_r))
    return









# example for minimizing the sphere function: integer continuous
if False:
    t1 = time.clock()
    # repeat of optimization experiments
    repeat = 5
    result = []
    # the random seed for zoopt can be set
    gl.set_seed(12345)
    for i in range(repeat):
        # setup optimization problem
        dim_size = 100  # dimensions
        dim_regs = [[-10, 10]] * dim_size  # dimension range
        dim_tys = [False] * dim_size  # dimension type : integer
        dim = Dimension(dim_size, dim_regs, dim_tys, order=True)  # form up the dimension object
        objective = Objective(sphere_integer, dim)  # form up the objective function

        # setup algorithm parameters
        budget = 100000  # number of calls to the objective function
        parameter = Parameter(budget=budget, sequential=True,
                              intermediate_result=False)  # by default, the algorithm is sequential RACOS

        # perform the optimization
        solution = Opt.min(objective, parameter)

        # store the optimization result
        print('solved solution is:')
        solution.print_solution()
        result.append(solution.get_value())

        ### to plot the optimization history, uncomment the following codes.
        ### matplotlib is required
        # plt.plot(objective.get_history_bestsofar())
        # plt.savefig("figure.png")

    result_analysis(result, 1)
    t2 = time.clock()
    print('time costed %f seconds' % (t2 - t1))




