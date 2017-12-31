"""
This file contains an example of how to optimize continuous ackley function.

Author:
    Yu-Ren Liu, Xiong-Hui Chen
"""

from zoopt import Dimension, Objective, Parameter, Opt, Solution
import matplotlib.pyplot as plt
from fx import ackley
import numpy as np


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

if __name__ == '__main__':
    dim = 100 # dimension
    obj = Objective(ackley, Dimension(dim, [[-1, 1]] * dim, [True] * dim))  # setup objective
    # perform optimization
    solution = Opt.min(obj, Parameter(budget=100 * dim))
    # print result
    solution.print_solution()
    # a function to print optimization results
    plt.plot(obj.get_history_bestsofar())
    plt.savefig('img/quick_start.png')

