"""
This module contains an example of optimizing high-dimensional sphere function with sequential random embedding.

Author:
    Yu-Ren Liu
"""

import time
import numpy as np
from fx import sphere_sre
from zoopt import Dimension, Objective, Parameter, Opt, Solution
from zoopt.utils.zoo_global import gl
import matplotlib.pyplot as plt

def result_analysis(results, top):
    """
    Get mean value and standard deviation of best 'top' results.

    :param results: a list of results
    :param top: the number of best results used to calculate mean value and standard deviation
    :return: no return
    """
    limit = top if top < len(results) else len(results)
    results.sort()
    top_k = results[0:limit]
    mean_r = np.mean(top_k, dtype=np.float64)
    std_r = np.std(top_k, dtype=np.float64)
    print('%f +- %f' % (float(mean_r), float(std_r)))
    return


def sphere_continuous_sre():
    """
    Example of minimizing high-dimensional sphere function with sequential random embedding.

    :return: no result
    """
    t1 = time.clock()
    # repeat of optimization experiments
    repeat = 1
    result = []
    # the random seed for zoopt can be set
    gl.set_seed(12345)
    for i in range(repeat):
        # setup optimization problem
        dim_size = 10000  # dimensions
        dim_regs = [[-1, 1]] * dim_size  # dimension range
        dim_tys = [True] * dim_size  # dimension type : real
        dim = Dimension(dim_size, dim_regs, dim_tys)  # form up the dimension object
        objective = Objective(sphere_sre, dim, sre=True)  # form up the objective function

        # setup algorithm parameters
        budget = 5000  # number of calls to the objective function
        parameter = Parameter(budget=budget, num_sre=5, low_dimension=Dimension(10, [[-1, 1]] * 10, [True] * 10),
                              withdraw_alpha=Dimension(1, [[-1, 1]], [True]), intermediate_result=False, intermediate_freq=100)
        # perform the optimization
        solution = Opt.min(objective, parameter)

        # store the optimization result
        print('solved solution is:')
        solution.print_solution()
        result.append(solution.get_value())

        history = np.array(objective.get_history_bestsofar())  # init for reducing
        plt.plot(history)
    # plt.show()
    plt.savefig("img/sphere_continuous_sre.png")  # uncomment this line and comment last line to save figures
    result_analysis(result, 1)
    t2 = time.clock()
    print('time costed %f seconds' % (t2 - t1))


if __name__ == "__main__":
    sphere_continuous_sre()
