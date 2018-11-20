"""
This module contains an example of optimizing high-dimensional sphere function with sequential random embedding.

Author:
    Yu-Ren Liu
"""

from sphere_sre import sphere_sre
from zoopt import Dimension, Objective, Parameter, ExpOpt


def minimize_sphere_sre():
    """
    Example of minimizing high-dimensional sphere function with sequential random embedding.

    :return: no return value
    """

    dim_size = 10000  # dimensions
    dim_regs = [[-1, 1]] * dim_size  # dimension range
    dim_tys = [True] * dim_size  # dimension type : real
    dim = Dimension(dim_size, dim_regs, dim_tys)  # form up the dimension object
    objective = Objective(sphere_sre, dim)  # form up the objective function

    # setup algorithm parameters
    budget = 2000  # number of calls to the objective function
    parameter = Parameter(budget=budget, high_dim_handling=True, reducedim=True, num_sre=5,
                          low_dimension=Dimension(10, [[-1, 1]] * 10, [True] * 10))
    solution_list = ExpOpt.min(objective, parameter, repeat=5, plot=False, plot_file="img/minimize_sphere_sre.png")


if __name__ == "__main__":
    minimize_sphere_sre()
