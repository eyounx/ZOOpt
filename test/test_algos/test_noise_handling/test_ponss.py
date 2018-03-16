from zoopt import Solution, Objective, Parameter, Opt
from zoopt.algos.noise_handling.ponss import PONSS
from sparse_mse import SparseMSE
from math import exp


class TestPONSS(object):
    def test_theta_dominate(self):
        sol1 = Solution(value=[1, 2])
        sol2 = Solution(value=[4, 2])
        assert PONSS.theta_dominate(2.9, sol1, sol2) is True and PONSS.theta_dominate(3, sol1, sol2) is False
        sol3 = Solution(value=[2, 3])
        sol4 = Solution(value=[3, 2])
        assert PONSS.theta_dominate(1, sol1, sol2) is True

    def test_theta_weak_dominate(self):
        sol1 = Solution(value=[1, 2])
        sol2 = Solution(value=[4, 2])
        assert PONSS.theta_weak_dominate(3, sol1, sol2) is True
        assert PONSS.theta_weak_dominate(3.1, sol1, sol2) is False

    def test_performance(self):
        # load data file
        mse = SparseMSE('example/sparse_regression/sonar.arff')
        mse.set_sparsity(8)

        # setup objective
        objective = Objective(func=mse.loss, dim=mse.get_dim(), constraint=mse.constraint)
        # ponss_theta and ponss_b are parameters used in PONSS algorithm and should be provided by users. ponss_theta stands
        # for the threshold. ponss_b limits the number of solutions in the population set.
        parameter = Parameter(algorithm='poss', noise_handling=True, ponss=True, ponss_theta=0.5, ponss_b=mse.get_k(),
                              budget=2 * exp(1) * (mse.get_sparsity() ** 2) * mse.get_dim().get_size())

        # perform sparse regression with constraint |w|_0 <= k
        solution = Opt.min(objective, parameter)
        assert solution.get_value()[0] < 0.7
