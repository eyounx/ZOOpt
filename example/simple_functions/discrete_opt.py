"""
This file contains examples of optimizing discrete objective function.

Author:
    Yu-Ren Liu
"""

from simple_function import SetCover
from zoopt import Dimension, Objective, Parameter, ExpOpt


def minimize_setcover_discrete():
    """
    Discrete optimization example of minimizing setcover problem.

    :return: no return value
    """
    problem = SetCover()
    dim = problem.dim  # the dim is prepared by the class
    objective = Objective(problem.fx, dim)  # form up the objective function
    budget = 100 * dim.get_size()  # number of calls to the objective function
    # if autoset is False, you should define train_size, positive_size, negative_size on your own
    parameter = Parameter(budget=budget, autoset=False)
    parameter.set_train_size(6)
    parameter.set_positive_size(1)
    parameter.set_negative_size(5)

    ExpOpt.min(objective, parameter, repeat=10, best_n=5, plot=True, plot_file="img/setcover_discrete_figure.png")


if __name__ == '__main__':
    minimize_setcover_discrete()
