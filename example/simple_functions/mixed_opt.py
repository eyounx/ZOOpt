import matplotlib.pyplot as plt
import time
import numpy as np
from fx import sphere, ackley, setcover, sphere_mixed, ackley_noise_creator
from zoopt import Dimension, Objective, Parameter, Opt, Solution
from zoopt.utils.zoo_global import gl
from quick_start import result_analysis

# # mixed optimization
# if False:
#     repeat = 15
#     result = []
#     gl.set_seed(12345)
#     for j in range(repeat):
#         dim_size = 10
#         dim_regs = []
#         dim_tys = []
#         # In this example, the search space is discrete if this dimension index is odd, Otherwise, the search space
#         # is continuous.
#         for i in range(dim_size):
#             if i % 2 == 0:
#                 dim_regs.append([0, 1])
#                 dim_tys.append(True)
#             else:
#                 dim_regs.append([0, 100])
#                 dim_tys.append(False)
#         dim = Dimension(dim_size, dim_regs, dim_tys)
#         objective = Objective(mixed_function, dim)
#         budget = 2000
#         parameter = Parameter(budget=budget, autoset=True)
#         solution = Opt.min(objective, parameter)
#         solution.print_solution()
#         result.append(solution.get_value())
#     result_analysis(result, 5)


# mixed optimization
def minimize_sphere_mixed():
    t1 = time.clock()
    gl.set_seed(12345)  # set random seed
    repeat = 10  # repeat of optimization experiments
    result = []
    history = []
    for i in range(repeat):
        # setup optimization problem
        dim_size = 10
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
        budget = 2000  # number of calls to the objective function
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
    plt.savefig("sphere_mixed_figure.png")  # uncomment this line to save figures
    result_analysis(result, 5)
    t2 = time.clock()
    print('time cost: %f' % (t2 - t1))

if __name__ == '__main__':
    minimize_sphere_mixed()