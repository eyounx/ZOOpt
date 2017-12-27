import matplotlib.pyplot as plt
import time
import numpy as np
from fx import sphere_discrete_order
from zoopt import Dimension, Objective, Parameter, Opt, Solution
from zoopt.utils.zoo_global import gl
from quick_start import result_analysis


# # example for minimizing the discrete sphere function which has order relation in search space
# if False:
#     t1 = time.clock()
#     # repeat of optimization experiments
#     repeat = 5
#     result = []
#     # the random seed for zoopt can be set
#     gl.set_seed(12345)
#     for i in range(repeat):
#         # setup optimization problem
#         dim_size = 100  # dimensions
#         dim_regs = [[-10, 10]] * dim_size  # dimension range
#         dim_tys = [False] * dim_size  # dimension type : integer
#         dim = Dimension(dim_size, dim_regs, dim_tys, order=True)  # form up the dimension object
#         objective = Objective(sphere_discrete_order, dim)  # form up the objective function
#
#         # setup algorithm parameters
#         budget = 100000  # number of calls to the objective function
#         parameter = Parameter(budget=budget, sequential=True,
#                               intermediate_result=False)  # by default, the algorithm is sequential RACOS
#
#         # perform the optimization
#         solution = Opt.min(objective, parameter)
#
#         # store the optimization result
#         print('solved solution is:')
#         solution.print_solution()
#         result.append(solution.get_value())
#
#         ### to plot the optimization history, uncomment the following codes.
#         ### matplotlib is required
#         # plt.plot(objective.get_history_bestsofar())
#         # plt.savefig("figure.png")
#
#     result_analysis(result, 1)
#     t2 = time.clock()
#     print('time costed %f seconds' % (t2 - t1))

# example for minimizing the ackley function
def minimize_sphere_discrete_order():
    t1 = time.clock()
    gl.set_seed(12345)  # set random seed
    repeat = 1  # repeat of optimization experiments
    result = []
    history = []
    for i in range(repeat):
        # setup optimization problem
        dim_size = 100  # dimensions
        dim_regs = [[-10, 10]] * dim_size  # dimension range
        dim_tys = [False] * dim_size  # dimension type : integer
        dim = Dimension(dim_size, dim_regs, dim_tys, order=True)  # form up the dimension object
        objective = Objective(sphere_discrete_order, dim)  # form up the objective function

        # setup algorithm parameters
        budget = 10000  # number of calls to the objective function
        parameter = Parameter(budget=budget)

        # perform the optimization
        solution = Opt.min(objective, parameter)

        print('solved solution is:')
        solution.print_solution()
        # store the optimization result
        result.append(solution.get_value())

        # for plotting the optimization history
        if i == 0:
            history.append([0 for k in range(budget)])  # init for reducing
        history.append(objective.get_history_bestsofar())
    average_regret = reduce(lambda x, y: np.array(x) + np.array(y), history) / repeat  # get average regret
    plt.plot(average_regret)
    # plt.show()
    plt.savefig("sphere_discrete_order_figure.png")  # uncomment this line to save figures
    result_analysis(result, 1)
    t2 = time.clock()
    print('time cost: %f' % (t2 - t1))

if __name__ == '__main__':
    minimize_sphere_discrete_order()
