from zoopt import Dimension, Objective, Parameter, Opt, ExpOpt
import numpy as np


class TestPerformance(object):
    def test_sphere(object):
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

        dim = 100  # dimension
        objective = Objective(ackley, Dimension(dim, [[-1, 1]] * dim, [True] * dim))  # setup objective
        parameter = Parameter(budget=100 * dim)
        solution = Opt.min(objective, parameter)
        assert solution.get_value() < 0.2

        parameter = Parameter(budget=100 * dim, sequential=False)
        solution = ExpOpt.min(objective, parameter)[0]
        assert solution.get_value() < 0.2

