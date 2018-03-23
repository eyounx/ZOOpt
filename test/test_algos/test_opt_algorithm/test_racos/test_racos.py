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


class TestRacos(object):
    def test_racos_common_extend(self):
        a = [1, 2, 3]
        b = [2, 3, 4]
        assert RacosCommon.extend(a, b) == [1, 2, 3, 2, 3, 4]

    def test_racos_common_is_distinct(self):
        a = Solution(x=[1, 2, 3])
        b = Solution(x=[2, 3, 4])
        c = Solution(x=[3, 4, 5])
        seti = [a, b]
        assert RacosCommon.is_distinct(seti, a) is False and RacosCommon.is_distinct(seti, c) is True

    def test_sracos_distance(self):
        a = [2, 4]
        b = [5, 8]
        assert SRacos.distance(a, b) == 5

    def test_sracos_binary_search(self):
        s0 = Solution(value=0)
        s1 = Solution(value=1)
        s2 = Solution(value=2)
        s3 = Solution(value=3)
        s4 = Solution(value=4)
        # 1 3 0 2 4
        test_s1 = Solution(value=2.1)
        test_s2 = Solution(value=4.5)
        test_s3 = Solution(value=-1)
        test_s4 = Solution(value=2)
        set = [s0, s1, s2, s3, s4]
        sracos = SRacos()
        assert sracos.binary_search(set, test_s1, 0, 4) == 3
        assert sracos.binary_search(set, test_s1, 0, 2) == 3
        assert sracos.binary_search(set, test_s2, 0, 4) == 5
        assert sracos.binary_search(set, test_s3, 0, 4) == 0
        assert sracos.binary_search(set, test_s4, 0, 4) == 3

    def test_sracos_strategy_wr(self):
        s0 = Solution(value=0)
        s1 = Solution(value=1)
        s2 = Solution(value=2)
        s3 = Solution(value=3)
        s4 = Solution(value=4)
        iset = [s0, s1, s2, s3, s4]
        sracos = SRacos()
        test_s1 = Solution(value=2.1)
        sracos.strategy_wr(iset, test_s1, 'pos')
        assert len(iset) == 5 and iset[0].get_value() == 0 and iset[1].get_value() == 1 and iset[2].get_value() == 2 \
            and iset[3].get_value() == 2.1 and iset[4].get_value() == 3
        iset2 = [s1, s3, s0, s2, s4]
        sracos.strategy_wr(iset2, test_s1, 'neg')
        assert len(iset2) == 5 and iset2[4].get_value() == 2.1

    def test_sracos_strategy_rr(self):
        s0 = Solution(value=0)
        s1 = Solution(value=1)
        s2 = Solution(value=2)
        iset = [s0, s1, s2]
        sracos = SRacos()
        test_s1 = Solution(value=2.1)
        sracos.strategy_rr(iset, test_s1)
        assert len(iset) == 3 and (iset[0].get_value() == 2.1 or iset[1].get_value() == 2.1 or iset[2].get_value() == 2.1)

    def test_sracos_strategy_lm(self):
        s0 = Solution(x=[1, 1, 1], value=0)
        s1 = Solution(x=[2.2, 2.2, 2.2], value=1)
        s2 = Solution(x=[3, 3, 3], value=2)
        iset = [s0, s1, s2]
        sracos = SRacos()
        test_s1 = Solution(x=[2.1, 2.1, 2.1], value=2.1)
        sracos.strategy_lm(iset, s0, test_s1)
        assert iset[2].get_value() == 2.1

    def test_sracos_replace(self):
        s0 = Solution(x=[0, 0, 0], value=0.5)
        s1 = Solution(x=[1, 1, 1], value=1)
        s2 = Solution(x=[2, 2, 2], value=2)
        s3 = Solution(x=[3, 3, 3], value=3)
        s4 = Solution(x=[4, 4, 4], value=4)
        pos_set = [s0, s1, s2, s3, s4]
        neg_set = [s2, s3, s1, s4, s0]
        x = Solution(x=[2.1, 2.1, 2.1], value=0.1)
        sracos = SRacos()
        sracos.replace(pos_set, x, 'pos', 'WR')
        assert pos_set[4].get_value() == 3 and pos_set[0].get_value() == 0.1
        sracos.replace(neg_set, x, 'neg', 'LM')
        assert neg_set[3].get_value() == 0.1

    def test_racos_performance(self):
        dim = 100  # dimension
        objective = Objective(ackley, Dimension(dim, [[-1, 1]] * dim, [True] * dim))  # setup objective
        parameter = Parameter(budget=100 * dim, sequential=False)
        solution = ExpOpt.min(objective, parameter)[0]
        assert solution.get_value() < 0.2

    def test_sracos_performance(self):
        dim = 100  # dimension
        objective = Objective(ackley, Dimension(dim, [[-1, 1]] * dim, [True] * dim))  # setup objective
        parameter = Parameter(budget=100 * dim)
        solution = Opt.min(objective, parameter)
        assert solution.get_value() < 0.2

