import numpy as np
from zoopt import Dimension, Objective, Parameter, Opt


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


def ackley_noise_creator(mu, sigma):
    """
    Ackley function under noise
    """
    return lambda solution: ackley(solution) + np.random.normal(mu, sigma, 1)


class TestSSRacos(object):
    def test_performance(self):
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
        parameter = Parameter(budget=budget, noise_handling=True, suppression=True, non_update_allowed=200,
                              resample_times=50, balance_rate=0.5)

        # parameter = Parameter(budget=budget, noise_handling=True, resampling=True, resample_times=10)
        parameter.set_positive_size(5)

        sol = Opt.min(objective, parameter)
        assert sol.get_value() < 4

    def test_resample(self):
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
        parameter = Parameter(budget=budget, noise_handling=True, resampling=True, resample_times=10)

        # parameter = Parameter(budget=budget, noise_handling=True, resampling=True, resample_times=10)
        parameter.set_positive_size(5)

        sol = Opt.min(objective, parameter)
        assert sol.get_value() < 4