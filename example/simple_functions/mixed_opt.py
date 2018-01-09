"""
This file contains an example of optimizing a function with the mixed search space(continuous and discrete).

Author:
    Yu-Ren Liu
"""
from simple_function import sphere_mixed
from zoopt import Dimension, Objective, Parameter, ExpOpt


# mixed optimization
def minimize_sphere_mixed():
    """
    Mixed optimization example of minimizing sphere function, which has mixed search search space.

    :return: no return value
    """

    # setup optimization problem
    dim_size = 100
    dim_regs = []
    dim_tys = []
    # In this example, the search space is discrete if this dimension index is odd, Otherwise, the search space
    # is continuous.
    for i in range(dim_size):
        if i % 2 == 0:
            dim_regs.append([0, 1])
            dim_tys.append(True)
        else:
            dim_regs.append([0, 100])
            dim_tys.append(False)
    dim = Dimension(dim_size, dim_regs, dim_tys)
    objective = Objective(sphere_mixed, dim)  # form up the objective function
    budget = 100 * dim_size  # number of calls to the objective function
    parameter = Parameter(budget=budget)

    solution_list = ExpOpt.min(objective, parameter, repeat=1, plot=True, plot_file="img/sphere_mixed_figure.png")

if __name__ == '__main__':
    minimize_sphere_mixed()
