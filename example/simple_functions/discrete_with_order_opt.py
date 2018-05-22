"""
This file contains examples of optimizing discrete objective function with ordered search space.

Author:
    Yu-Ren Liu
"""

from simple_function import sphere_discrete_order
from zoopt import Dimension, Objective, Parameter, ExpOpt


def minimize_sphere_discrete_order():
    """
    Discrete optimization example of minimizing the sphere function, which has ordered search space.

    :return: no return value
    """
    dim_size = 100  # dimensions
    dim_regs = [[-10, 10]] * dim_size  # dimension range
    dim_tys = [False] * dim_size  # dimension type : integer
    dim_order = [True] * dim_size
    dim = Dimension(dim_size, dim_regs, dim_tys, order=dim_order)  # form up the dimension object
    objective = Objective(sphere_discrete_order, dim)  # form up the objective function

    # setup algorithm parameters
    budget = 10000  # number of calls to the objective function
    parameter = Parameter(budget=budget)

    ExpOpt.min(objective, parameter, repeat=1, plot=True, plot_file="img/sphere_discrete_order_figure.png")


if __name__ == '__main__':
    minimize_sphere_discrete_order()
