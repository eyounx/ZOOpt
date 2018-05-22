"""
This file contains examples of optimizing continuous objective function.

Author:
    Yu-Ren Liu, Xiong-Hui Chen
"""


from simple_function import sphere, ackley
from zoopt import Dimension, Objective, Parameter, ExpOpt


def minimize_ackley_continuous():
    """
    Continuous optimization example of minimizing the ackley function.

    :return: no return value
    """
    dim_size = 100  # dimensions
    dim_regs = [[-1, 1]] * dim_size  # dimension range
    dim_tys = [True] * dim_size  # dimension type : real
    dim = Dimension(dim_size, dim_regs, dim_tys)  # form up the dimension object

    objective = Objective(ackley, dim)  # form up the objective function

    budget = 100 * dim_size  # number of calls to the objective function
    parameter = Parameter(budget=budget)

    solution_list = ExpOpt.min(objective, parameter, repeat=1, plot=True, plot_file="img/ackley_continuous_figure.png")


def minimize_sphere_continuous():
    """
    Example of minimizing the sphere function

    :return: no return value
    """
    dim_size = 100
    # form up the objective function
    objective = Objective(sphere, Dimension(dim_size, [[-1, 1]] * dim_size, [True] * dim_size))

    budget = 100 * dim_size
    # if intermediate_result is True, ZOOpt will output intermediate best solution every intermediate_freq budget
    parameter = Parameter(budget=budget, intermediate_result=True,
                          intermediate_freq=1000)
    ExpOpt.min(objective, parameter, repeat=1, plot=True, plot_file="img/sphere_continuous_figure.png")


if __name__ == '__main__':
    minimize_ackley_continuous()
    # minimize_sphere_continuous()
