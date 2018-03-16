"""
This file contains an example of optimizing a function under noise.

Author:
    Xiong-Hui Chen, Yu-Ren Liu
"""

from simple_function import ackley, ackley_noise_creator
from zoopt import Dimension, Objective, Parameter, ExpOpt, Solution


def minimize_ackley_continuous_noisy():
    """
    SSRacos example of minimizing ackley function under Gaussian noise

    :return: no return value
    """
    ackley_noise_func = ackley_noise_creator(0, 0.1)
    dim_size = 100  # dimensions
    dim_regs = [[-1, 1]] * dim_size  # dimension range
    dim_tys = [True] * dim_size  # dimension type : real
    dim = Dimension(dim_size, dim_regs, dim_tys)  # form up the dimension object
    objective = Objective(ackley_noise_func, dim)  # form up the objective function
    budget = 20000  # 20*dim_size  # number of calls to the objective function
    # suppression=True means optimize with value suppression, which is a noise handling method
    # resampling=True means optimize with re-sampling, which is another common used noise handling method
    # non_update_allowed=500 and resample_times=100 means if the best solution doesn't change for 500 budgets,
    # the best solution will be evaluated repeatedly for 100 times
    # balance_rate is a parameter for exponential weight average of several evaluations of one sample.
    parameter = Parameter(budget=budget, noise_handling=True, suppression=True, non_update_allowed=200, resample_times=50, balance_rate=0.5)

    # parameter = Parameter(budget=budget, noise_handling=True, resampling=True, resample_times=10)
    parameter.set_positive_size(5)

    ExpOpt.min(objective, parameter, repeat=5, plot=False, plot_file="img/ackley_continuous_noisy_figure.png")

if __name__ == '__main__':
    minimize_ackley_continuous_noisy()
