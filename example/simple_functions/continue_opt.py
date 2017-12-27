import matplotlib.pyplot as plt
import time
import numpy as np
from fx import sphere, ackley, setcover, ackley_noise_creator
from zoopt import Dimension, Objective, Parameter, Opt, Solution
from zoopt.utils.zoo_global import gl
from quick_start import result_analysis


# example for minimizing the ackley function
def minimize_ackley_continuous():
    t1 = time.clock()
    gl.set_seed(12345)  # set random seed
    repeat = 1  # repeat of optimization experiments
    result = []
    history = []
    for i in range(repeat):
        # setup optimization problem
        dim_size = 100  # dimensions
        dim_regs = [[-1, 1]] * dim_size  # dimension range
        dim_tys = [True] * dim_size  # dimension type : real
        dim = Dimension(dim_size, dim_regs, dim_tys)  # form up the dimension object
        objective = Objective(ackley, dim)  # form up the objective function
        budget = 100 * dim_size  # number of calls to the objective function
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
    plt.show()
    # plt.savefig("ackley_continuous_figure.png")  # uncomment this line to save figures
    result_analysis(result, 1)
    t2 = time.clock()
    print('time cost: %f' % (t2 - t1))


# example for minimizing the sphere function
def minimize_sphere_continuous():
    gl.set_seed(12345)
    t1 = time.clock()
    repeat = 10
    result = []
    history = []
    for i in range(repeat):
        dim_size = 100
        # form up the objective function
        objective = Objective(sphere, Dimension(dim_size, [[-1, 1]] * dim_size, [True] * dim_size))

        budget = 100 * dim_size
        # if intermediate_result is True, ZOOpt will output intermediate best solution every intermediate_freq budget
        parameter = Parameter(budget=budget, intermediate_result=True,
                              intermediate_freq=1000)
        solution = Opt.min(objective, parameter)

        print('solved solution is:')
        solution.print_solution()
        result.append(solution.get_value())
        if i == 0:
            history.append([0 for k in range(budget)])
        history.append(objective.get_history_bestsofar())
    average_regret = reduce(lambda x, y: np.array(x) + np.array(y), history) / repeat  # get average regret
    plt.plot(average_regret)
    # plt.show()
    plt.savefig("sphere_continuous_figure.png")  # uncomment this line to save figures
    result_analysis(result, 5)
    t2 = time.clock()
    print('time cost: %f' % (t2 - t1))

if __name__ == '__main__':
    # minimize_ackley_continuous()
    minimize_sphere_continuous()
