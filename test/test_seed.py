from zoopt.algos.opt_algorithms.racos.racos_common import RacosCommon
from zoopt.algos.opt_algorithms.racos.sracos import SRacos
from zoopt import Solution, Objective, Dimension, Parameter, Opt, ExpOpt
import numpy as np


def ackley(solution):
    """
    Ackley function for continuous optimization
    """
    x = solution.get_x()
    bias = 0.2
    ave_seq = sum([(i - bias) * (i - bias) for i in x]) / len(x)
    ave_cos = sum([np.cos(2.0 * np.pi * (i - bias)) for i in x]) / len(x)
    value = -20 * np.exp(-0.2 * np.sqrt(ave_seq)) - np.exp(ave_cos) + 20.0 + np.e
    return value


def ackley_noise_creator(mu, sigma):
    """
    Ackley function under noise
    """
    return lambda solution: ackley(solution) + np.random.normal(mu, sigma, 1)

def sphere_sre(solution):
    """
    Variant of the sphere function. Dimensions except the first 10 ones have limited impact on the function value.
    """
    a = 0
    bias = 0.2
    x = solution.get_x()
    x1 = x[:10]
    x2 = x[10:]
    value1 = sum([(i-bias)*(i-bias) for i in x1])
    value2 = 1/len(x) * sum([(i-bias)*(i-bias) for i in x2])
    return value1 + value2

class TestSeed(object):
    # def test_racos(self):
    #     seed = 1
    #     dim = 100  # dimension
    #     objective = Objective(ackley, Dimension(dim, [[-1, 1]] * dim, [True] * dim))  # setup objective
    #     parameter = Parameter(budget=100 * dim, seed=seed, sequential=False)  # init with init_samples
    #     sol1 = Opt.min(objective, parameter)
    #     sol2 = Opt.min(objective, parameter)
    #     assert sol1.get_value() == sol2.get_value()
    #
    #
    # def test_sracos(self):
    #     seed = 1
    #     dim = 100  # dimension
    #     objective = Objective(ackley, Dimension(dim, [[-1, 1]] * dim, [True] * dim))  # setup objective
    #     parameter = Parameter(budget=100 * dim, seed=seed, sequential=True)  # init with init_samples
    #     sol1 = Opt.min(objective, parameter)
    #     sol2 = Opt.min(objective, parameter)
    #     assert sol1.get_value() == sol2.get_value()
    #
    def test_noisy(self):
        ackley_noise_func = ackley_noise_creator(0, 0.1)
        dim_size = 100  # dimensions
        dim_regs = [[-1, 1]] * dim_size  # dimension range
        dim_tys = [True] * dim_size  # dimension type : real
        dim = Dimension(dim_size, dim_regs, dim_tys)  # form up the dimension object
        objective = Objective(ackley_noise_func, dim)  # form up the objective function
        budget = 20000  # 20*dim_size  # number of calls to the objective function
        parameter = Parameter(budget=budget, noise_handling=True, suppression=True, non_update_allowed=200,
                              resample_times=50, balance_rate=0.5, seed=1)

        # parameter = Parameter(budget=budget, noise_handling=True, resampling=True, resample_times=10)
        parameter.set_positive_size(5)
        sol1 = Opt.min(objective, parameter)
        sol2 = Opt.min(objective, parameter)
        assert sol1.get_value() == sol2.get_value()

    def test_high_dim(self):
        dim_size = 10000  # dimensions
        dim_regs = [[-1, 1]] * dim_size  # dimension range
        dim_tys = [True] * dim_size  # dimension type : real
        dim = Dimension(dim_size, dim_regs, dim_tys)  # form up the dimension object
        objective = Objective(sphere_sre, dim)  # form up the objective function

        # setup algorithm parameters
        budget = 2000  # number of calls to the objective function
        parameter = Parameter(budget=budget, high_dim_handling=True, reducedim=True, num_sre=5,
                              low_dimension=Dimension(10, [[-1, 1]] * 10, [True] * 10), seed=1)
        sol1 = Opt.min(objective, parameter)
        sol2 = Opt.min(objective, parameter)
        assert sol1.get_value() == sol2.get_value()


