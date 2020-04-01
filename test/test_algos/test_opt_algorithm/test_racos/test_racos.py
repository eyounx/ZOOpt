from zoopt.algos.opt_algorithms.racos.racos_common import RacosCommon
from zoopt.algos.opt_algorithms.racos.sracos import SRacos
from zoopt import Solution, Objective, Dimension, Parameter, Opt, ExpOpt, ValueType, Dimension2
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


def sphere_discrete_order(solution):
    """
    Sphere function for integer continuous optimization
    """
    x = solution.get_x()
    value = sum([(i-2)*(i-2) for i in x])
    return value

class SetCover:
    """
    set cover problem for discrete optimization
    this problem has some extra initialization tasks, thus we define this problem as a class
    """

    def __init__(self):
        self.__weight = [0.8356, 0.5495, 0.4444, 0.7269, 0.9960, 0.6633, 0.5062, 0.8429, 0.1293, 0.7355,
                         0.7979, 0.2814, 0.7962, 0.1754, 0.0267, 0.9862, 0.1786, 0.5884, 0.6289, 0.3008]
        self.__subset = []
        self.__subset.append([0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0])
        self.__subset.append([0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0])
        self.__subset.append([1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0])
        self.__subset.append([0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0])
        self.__subset.append([1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1])
        self.__subset.append([0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0])
        self.__subset.append([0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0])
        self.__subset.append([0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0])
        self.__subset.append([0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0])
        self.__subset.append([0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1])
        self.__subset.append([0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0])
        self.__subset.append([0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1])
        self.__subset.append([1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1])
        self.__subset.append([1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1])
        self.__subset.append([0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1])
        self.__subset.append([1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0])
        self.__subset.append([1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1])
        self.__subset.append([0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1])
        self.__subset.append([0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0])
        self.__subset.append([0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1])

    def fx(self, solution):
        """
        Objective function.

        :param solution: a Solution object
        :return: the value of f(x)
        """
        x = solution.get_x()
        allweight = 0
        countw = 0
        for i in range(len(self.__weight)):
            allweight += self.__weight[i]

        dims = []
        for i in range(len(self.__subset[0])):
            dims.append(False)

        for i in range(len(self.__subset)):
            if x[i] == 1:
                countw += self.__weight[i]
                for j in range(len(self.__subset[i])):
                    if self.__subset[i][j] == 1:
                        dims[j] = True
        full = True
        for i in range(len(dims)):
            if dims[i] is False:
                full = False

        if full is False:
            countw += allweight

        return countw

    @property
    def dim(self):
        """
        Dimension of set cover problem.
        :return: Dimension instance
        """
        dim_size = 20
        dim_regs = [[0, 1]] * dim_size
        dim_tys = [False] * dim_size
        return Dimension(dim_size, dim_regs, dim_tys)


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
        # continuous
        dim = 100  # dimension
        objective = Objective(ackley, Dimension(dim, [[-1, 1]] * dim, [True] * dim))  # setup objective
        parameter = Parameter(budget=100 * dim, sequential=False, seed=1)
        solution = ExpOpt.min(objective, parameter)[0]
        assert solution.get_value() < 0.2
        dim = 500
        objective = Objective(ackley, Dimension(dim, [[-1, 1]] * dim, [True] * dim))  # setup objective
        parameter = Parameter(budget=10000, sequential=False, seed=1)
        sol = Opt.min(objective, parameter)
        sol.print_solution()
        assert solution.get_value() < 2
        # discrete
        # setcover
        problem = SetCover()
        dim = problem.dim  # the dim is prepared by the class
        objective = Objective(problem.fx, dim)  # form up the objective function
        budget = 100 * dim.get_size()  # number of calls to the objective function
        parameter = Parameter(budget=budget, sequential=False, seed=777)
        sol = Opt.min(objective, parameter)
        sol.print_solution()
        assert sol.get_value() < 2
        # sphere
        dim_size = 100  # dimensions
        dim_regs = [[-10, 10]] * dim_size  # dimension range
        dim_tys = [False] * dim_size  # dimension type : integer
        dim_order = [True] * dim_size
        dim = Dimension(dim_size, dim_regs, dim_tys, order=dim_order)  # form up the dimension object
        objective = Objective(sphere_discrete_order, dim)  # form up the objective function
        parameter = Parameter(budget=10000, sequential=False, seed=77)
        sol = Opt.min(objective, parameter)
        sol.print_solution()
        assert sol.get_value() < 200

    def test_racos_performance2(self):
        # continuous
        dim = 100  # dimension
        one_dim = (ValueType.CONTINUOUS, [-1, 1], 1e-6)
        dim_list = [(one_dim)] * dim
        objective = Objective(ackley, Dimension2(dim_list))  # setup objective
        parameter = Parameter(budget=100 * dim, sequential=False, seed=1)
        solution = ExpOpt.min(objective, parameter)[0]
        assert solution.get_value() < 0.2
        dim = 500
        dim_list = [(one_dim)] * dim
        objective = Objective(ackley, Dimension2(dim_list))  # setup objective
        parameter = Parameter(budget=10000, sequential=False, seed=1)
        sol = Opt.min(objective, parameter)
        sol.print_solution()
        assert solution.get_value() < 2
        # discrete
        # setcover
        problem = SetCover()
        dim_size = 20
        one_dim = (ValueType.DISCRETE, [0, 1], False)
        dim_list = [(one_dim)] * dim_size
        dim = Dimension2(dim_list)  # the dim is prepared by the class
        objective = Objective(problem.fx, dim)  # form up the objective function
        budget = 100 * dim.get_size()  # number of calls to the objective function
        parameter = Parameter(budget=budget, sequential=False, seed=777)
        sol = Opt.min(objective, parameter)
        sol.print_solution()
        assert sol.get_value() < 2
        # sphere
        dim_size = 100  # dimensions
        one_dim = (ValueType.DISCRETE, [-10, 10], True)
        dim_list = [(one_dim)] * dim_size
        dim = Dimension2(dim_list)  # form up the dimension object
        objective = Objective(sphere_discrete_order, dim)  # form up the objective function
        parameter = Parameter(budget=10000, sequential=False, seed=77)
        sol = Opt.min(objective, parameter)
        sol.print_solution()
        assert sol.get_value() < 200

    def test_sracos_performance(self):
        # continuous
        dim = 100  # dimension
        objective = Objective(ackley, Dimension(dim, [[-1, 1]] * dim, [True] * dim))  # setup objective
        parameter = Parameter(budget=100 * dim, seed=77)
        solution = Opt.min(objective, parameter)
        assert solution.get_value() < 0.2
        dim = 500
        objective = Objective(ackley, Dimension(dim, [[-1, 1]] * dim, [True] * dim))  # setup objective
        parameter = Parameter(budget=10000, seed=777)
        solution = Opt.min(objective, parameter)
        assert solution.get_value() < 1.5
        # discrete
        # setcover
        problem = SetCover()
        dim = problem.dim  # the dim is prepared by the class
        objective = Objective(problem.fx, dim)  # form up the objective function
        budget = 100 * dim.get_size()  # number of calls to the objective function
        parameter = Parameter(budget=budget, seed=777)
        sol = Opt.min(objective, parameter)
        assert sol.get_value() < 2
        # sphere
        dim_size = 100  # dimensions
        dim_regs = [[-10, 10]] * dim_size  # dimension range
        dim_tys = [False] * dim_size  # dimension type : integer
        dim_order = [True] * dim_size
        dim = Dimension(dim_size, dim_regs, dim_tys, order=dim_order)  # form up the dimension object
        objective = Objective(sphere_discrete_order, dim)  # form up the objective function
        parameter = Parameter(budget=10000)
        sol = Opt.min(objective, parameter)
        assert sol.get_value() < 200

    def test_sracos_performance2(self):
        # continuous
        dim = 100  # dimension
        one_dim = (ValueType.CONTINUOUS, [-1, 1], 1e-6)
        dim_list = [(one_dim)] * dim
        objective = Objective(ackley, Dimension2(dim_list))
        parameter = Parameter(budget=100 * dim, seed=77)
        solution = Opt.min(objective, parameter)
        assert solution.get_value() < 0.2
        dim = 500
        one_dim = (ValueType.CONTINUOUS, [-1, 1], 1e-6)
        dim_list = [(one_dim)] * dim
        objective = Objective(ackley, Dimension2(dim_list))  # setup objective
        parameter = Parameter(budget=10000, seed=777)
        solution = Opt.min(objective, parameter)
        assert solution.get_value() < 1.5
        # discrete
        # setcover
        problem = SetCover()
        dim_size = 20
        one_dim = (ValueType.DISCRETE, [0, 1], False)
        dim_list = [(one_dim)] * dim_size
        dim = Dimension2(dim_list)  # the dim is prepared by the class
        objective = Objective(problem.fx, dim)  # form up the objective function
        budget = 100 * dim.get_size()  # number of calls to the objective function
        parameter = Parameter(budget=budget, seed=777)
        sol = Opt.min(objective, parameter)
        assert sol.get_value() < 2
        # sphere
        dim_size = 100  # dimensions
        one_dim = (ValueType.DISCRETE, [-10, 10], True)
        dim_list = [(one_dim)] * dim_size
        dim = Dimension2(dim_list)  # form up the dimension object
        objective = Objective(sphere_discrete_order, dim)  # form up the objective function
        parameter = Parameter(budget=10000)
        sol = Opt.min(objective, parameter)
        assert sol.get_value() < 200

    def test_asracos_performance(self):
        # continuous
        dim = 100  # dimension
        objective = Objective(ackley, Dimension(dim, [[-1, 1]] * dim, [True] * dim))  # setup objective
        parameter = Parameter(budget=100 * dim, parallel=True, server_num=2, seed=2)
        # parameter = Parameter(budget=100 * dim, init_samples=[Solution([0] * 100)])  # init with init_samples
        solution_list = ExpOpt.min(objective, parameter, repeat=1)
        for solution in solution_list:
            value = solution.get_value()
            assert value < 0.2
        # discrete
        # setcover
        problem = SetCover()
        dim = problem.dim  # the dim is prepared by the class
        objective = Objective(problem.fx, dim)  # form up the objective function
        budget = 100 * dim.get_size()  # number of calls to the objective function
        parameter = Parameter(budget=budget, parallel=True, server_num=2, seed=777)
        sol = ExpOpt.min(objective, parameter, repeat=1)[0]
        assert sol.get_value() < 2
        # sphere
        dim_size = 100  # dimensions
        dim_regs = [[-10, 10]] * dim_size  # dimension range
        dim_tys = [False] * dim_size  # dimension type : integer
        dim_order = [True] * dim_size
        dim = Dimension(dim_size, dim_regs, dim_tys, order=dim_order)  # form up the dimension object
        objective = Objective(sphere_discrete_order, dim)  # form up the objective function
        parameter = Parameter(budget=10000, parallel=True, server_num=2, uncertain_bits=1, seed=1)
        sol = ExpOpt.min(objective, parameter)[0]
        assert sol.get_value() < 10
