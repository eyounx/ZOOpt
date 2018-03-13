from zoopt import Objective
from zoopt import Parameter
from zoopt import Dimension
from zoopt import Solution
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


class TestObjective(object):

    def test_parameter_set(self):
        par = Parameter(budget=1000, noise_handling=True, suppression=True)
        assert 1

    def test_eval(self):
        dim = 100
        obj = Objective(func=ackley, dim=Dimension(dim, [[-1, 1]] * dim, [True] * dim))
        sol = Solution(x=[0.2] * dim)
        res = obj.eval(sol)
        assert abs(res) <= 1e-7

    def test_resample(self):
        dim = 100
        obj = Objective(func=ackley, dim=Dimension(dim, [[-1, 1]] * dim, [True] * dim))
        sol = Solution(x=[0.2] * dim)
        res = obj.eval(sol)
        obj.resample(sol, 3)
        assert abs(sol.get_value()) <= 1e-7
        sol.set_value(0)
        obj.resample_func(sol, 3)
        assert abs(sol.get_value()) <= 1e-7

    def test_history_best_so_far(self):
        input_data = [0.5, 0.6, 0.4, 0.7, 0.3, 0.2]
        output_data = [0.5, 0.5, 0.4, 0.4, 0.3, 0.2]
        obj = Objective()
        obj.set_history(input_data)
        best_history = obj.get_history_bestsofar()
        assert best_history == output_data

