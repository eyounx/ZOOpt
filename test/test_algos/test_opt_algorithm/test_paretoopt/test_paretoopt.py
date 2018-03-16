from zoopt.algos.opt_algorithms.paretoopt.paretoopt import ParetoOpt
from zoopt import Objective, Parameter, Opt
from math import exp
from sparse_mse import SparseMSE


class TestParetoOpt(object):
    def test_mutation(self):
        a = [0, 1, 0, 1]
        n = 4
        res = ParetoOpt.mutation(a, n)
        assert res != a

    def test_performance(self):
        mse = SparseMSE('example/sparse_regression/sonar.arff')
        mse.set_sparsity(8)

        # setup objective
        # print(mse.get_dim().get_size())
        objective = Objective(func=mse.loss, dim=mse.get_dim(), constraint=mse.constraint)
        parameter = Parameter(algorithm='poss',
                              budget=2 * exp(1) * (mse.get_sparsity() ** 2) * mse.get_dim().get_size())

        # perform sparse regression with constraint |w|_0 <= k
        solution = Opt.min(objective, parameter)
        assert solution.get_value()[0] < 0.6
