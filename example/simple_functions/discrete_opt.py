import matplotlib.pyplot as plt  # uncomment this line to plot figures
import time
import numpy as np
from fx import sphere, ackley, setcover, ackley_noise_creator
from zoopt import Dimension, Objective, Parameter, Opt, Solution
from zoopt.utils.zoo_global import gl
from quick_start import result_analysis


# discrete optimization example using minimum set cover instance
def minimize_setcover_discrete():
    gl.set_seed(12345)
    t1 = time.clock()
    repeat = 1
    result = []
    history = []
    for i in range(repeat):
        problem = setcover()
        dim = problem.dim  # the dim is prepared by the class
        objective = Objective(problem.fx, dim)  # form up the objective function
        budget = 100 * dim.get_size()  # number of calls to the objective function
        # if autoset is False, you should define train_size, positive_size, negative_size on your own
        parameter = Parameter(budget=budget, autoset=False)
        parameter.set_train_size(6)
        parameter.set_positive_size(1)
        parameter.set_negative_size(5)

        print('solved solution is:')
        # perform the optimization
        solution = Opt.min(objective, parameter)
        solution.print_solution()
        # store the optimization result
        result.append(solution.get_value())

        # for plotting the optimization history
        if i == 0:
            history.append([0 for k in range(budget)])
        history.append(objective.get_history_bestsofar())
    average_regret = reduce(lambda x, y: np.array(x) + np.array(y), history) / repeat  # get average regret
    plt.plot(average_regret)
    # plt.show()
    plt.savefig("img/setcover_discrete_figure.png")  # uncomment this line and comment last line to save figures
    result_analysis(result, 1)
    t2 = time.clock()
    print('time cost: %f' % (t2 - t1))

if __name__ == '__main__':
    minimize_setcover_discrete()