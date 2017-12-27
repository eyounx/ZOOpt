import matplotlib.pyplot as plt
import time
import numpy as np
from fx import sphere_discrete_order
from zoopt import Dimension, Objective, Parameter, Opt, Solution
from zoopt.utils.zoo_global import gl
from quick_start import result_analysis

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
    plt.savefig("img/sphere_discrete_order_figure.png")  # uncomment this line and comment last line to save figures
    result_analysis(result, 1)
    t2 = time.clock()
    print('time cost: %f' % (t2 - t1))

if __name__ == '__main__':
    minimize_sphere_discrete_order()
