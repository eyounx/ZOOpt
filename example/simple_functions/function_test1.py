"""
This file contains examples of optimizing discrete objective function.

Author:
    Yu-Ren Liu
"""

from simple_function import SetCover, sphere_discrete_order, ackley
from zoopt import Dimension, Objective, Parameter, ExpOpt, Opt


# continuous
# dim = 100  # dimension
# objective = Objective(ackley, Dimension(dim, [[-1, 1]] * dim, [True] * dim))  # setup objective
# parameter = Parameter(budget=100 * dim, parallel=True, server_num=2)
# # parameter = Parameter(budget=100 * dim, init_samples=[Solution([0] * 100)])  # init with init_samples
# solution_list = ExpOpt.min(objective, parameter, repeat=1)
# for solution in solution_list:
#     value = solution.get_value()
#     assert value < 0.2
# discrete
# setcover
problem = SetCover()
dim = problem.dim  # the dim is prepared by the class
objective = Objective(problem.fx, dim)  # form up the objective function
budget = 100 * dim.get_size()  # number of calls to the objective function
parameter = Parameter(budget=budget, parallel=True, server_num=2, seed=1)
solution_list = ExpOpt.min(objective, parameter, repeat=10)
for solution in solution_list:
    value = solution.get_value()
    assert value < 2
# # sphere
# dim_size = 100  # dimensions
# dim_regs = [[-10, 10]] * dim_size  # dimension range
# dim_tys = [False] * dim_size  # dimension type : integer
# dim_order = [True] * dim_size
# dim = Dimension(dim_size, dim_regs, dim_tys, order=dim_order)  # form up the dimension object
# objective = Objective(sphere_discrete_order, dim)  # form up the objective function
# parameter = Parameter(budget=1000, parallel=True, server_num=1)
# solution_list = ExpOpt.min(objective, parameter, repeat=2, plot=True)
# for solution in solution_list:
#     value = solution.get_value()

# sphere
# dim_size = 100  # dimensions
# dim_regs = [[-10, 10]] * dim_size  # dimension range
# dim_tys = [False] * dim_size  # dimension type : integer
# dim_order = [True] * dim_size
# dim = Dimension(dim_size, dim_regs, dim_tys, order=dim_order)  # form up the dimension object
# objective = Objective(sphere_discrete_order, dim)  # form up the objective function
# parameter = Parameter(budget=10000)
# sol = ExpOpt.min(objective, parameter, repeat=5, plot=True)

