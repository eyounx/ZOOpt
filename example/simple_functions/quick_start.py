"""
This file contains an example of how to optimize continuous ackley function.

Author:
    Yu-Ren Liu, Xiong-Hui Chen
"""

from zoopt import Dimension, Objective, Parameter, ExpOpt, Solution
from simple_function import ackley

if __name__ == '__main__':
    dim = 100  # dimension
    objective = Objective(ackley, Dimension(dim, [[-1, 1]] * dim, [True] * dim))  # setup objective
    parameter = Parameter(budget=100 * dim, init_samples=[Solution([0] * 100)])  # init with init_samples
    solution_list = ExpOpt.min(objective, parameter, repeat=5, plot=False, plot_file="img/quick_start.png")
    for solution in solution_list:
        x = solution.get_x()
        value = solution.get_value()
        print(x, value)