"""
This file contains some examples about how to use Racos(or SRacos)
optimization algorithm

Author:
    Yuren Liu, Xionghui Chen
"""

from zoopt import Dimension, Objective, Parameter, Opt, Solution
import matplotlib.pyplot as plt
from fx import ackley
import numpy as np


def result_analysis(result, top):
    limit = top if top < len(result) else len(result)
    result.sort()
    top_k = result[0:limit]
    mean_r = np.mean(top_k)
    std_r = np.std(top_k)
    print('%f +- %f' % (mean_r, std_r))
    return

if __name__ == '__main__':
    dim = 100 # dimension
    obj = Objective(ackley, Dimension(dim, [[-1, 1]] * dim, [True] * dim)) # setup objective
    # perform optimization
    solution = Opt.min(obj, Parameter(budget=100 * dim))
    # print result
    solution.print_solution()
    # a function to print optimization results
    plt.plot(obj.get_history_bestsofar())
    plt.savefig('img/quick_start.png')

