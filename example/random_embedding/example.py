import time
import numpy as np
from fx import sphere_re
from zoopt import Dimension, Objective, Parameter, Opt, Solution
from zoopt.utils.zoo_global import gl


# a function to print optimization results
def result_analysis(result, top):
    result.sort()
    top_k = result[0:top]
    mean_r = np.mean(top_k)
    std_r = np.std(top_k)
    print('%f +- %f' % (mean_r, std_r))
    return


# example for minimizing the sphere function with random embedding
if True:
    t1 = time.clock()
    # repeat of optimization experiments
    repeat = 1
    result = []
    # the random seed for zoopt can be set
    gl.set_seed(12345)
    for i in range(repeat):
        # setup optimization problem
        dim_size = 2000  # dimensions
        dim_regs = [[-1, 1]] * dim_size  # dimension range
        dim_tys = [True] * dim_size  # dimension type : real
        dim = Dimension(dim_size, dim_regs, dim_tys)  # form up the dimension object
        objective = Objective(sphere_re, dim, sre=True)  # form up the objective function

        # setup algorithm parameters
        budget = 10000 # number of calls to the objective function
        parameter = Parameter(budget=budget, num_sre=5, low_dimension=Dimension(10, [[-1, 1]] * 10, [True] * 10),
                              withdraw_alpha=Dimension(1, [[-1, 1]], [True]), intermediate_result=False, intermediate_freq=100)
        # perform the optimization
        solution = Opt.min(objective, parameter)

        # store the optimization result
        print('solved solution is:')
        solution.print_solution()
        result.append(solution.get_value())

        # to plot the optimization history, uncomment the following codes.
        # matplotlib is required
        # plt.plot(objective.get_history_bestsofar())
        # plt.savefig("figure.png")

    result_analysis(result, 1)
    t2 = time.clock()
    print('time costed %f seconds' % (t2 - t1))