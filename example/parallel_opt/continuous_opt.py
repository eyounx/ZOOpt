from zoopt import Objective, Dimension, Solution, Parameter, ExpOpt, Opt
import numpy as np


def ackley(solution):
    """
    Ackley function for continuous optimization
    """
    x = solution.get_x()
    bias = 0.2
    ave_seq = sum([(i - bias) * (i - bias) for i in x]) / len(x)
    ave_cos = sum([np.cos(2.0*np.pi*(i-bias)) for i in x]) / len(x)
    value = -20 * np.exp(-0.2 * np.sqrt(ave_seq)) - np.exp(ave_cos) + 20.0 + np.e
    return value


if __name__ == '__main__':
    dim = 100  # dimension
    objective = Objective(ackley, Dimension(dim, [[-1, 1]] * dim, [True] * dim))  # setup objective
    parameter = Parameter(budget=10000, parallel=True, server_num=3)  # init with init_samples
    sol = Opt.min(objective, parameter)
    print(sol.get_x())
    print(sol.get_value())
