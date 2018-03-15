from zoopt.algos.opt_algorithms.paretoopt.paretoopt import ParetoOpt


class TestParetoOpt(object):
    def test_mutation(self):
        a = [0, 1, 0, 1]
        n = 4
        res = ParetoOpt.mutation(a, n)
        assert res != a
