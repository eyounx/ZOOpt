"""
This module contains the class RacosCommon, which is a common part in Racos, SRacos and SSRacos.

Author:
    Yu-Ren Liu
"""

import copy, math
from zoopt.utils.tool_function import ToolFunction
from zoopt.solution import Solution


class RacosCommon:
    """
    This class contains common attributes and methods shared by Racos, SRacos and SSRacos.
    """
    def __init__(self):
        """
        Initialization.
        """
        self._parameter = None
        self._objective = None
        # Solution set
        # Random sampled solutions construct self._data
        self._data = []
        # self._positive_data are best-positive_size solutions set
        self._positive_data = []
        # self._negative_data are the other solutions
        self._negative_data = []
        # Solution
        self._best_solution = None
        self._possible_solution_list = []
        return

    def clear(self):
        """
        Clear RacosCommon.

        :return: no return value
        """
        self._parameter = None
        self._objective = None
        # Solution
        self._data = []
        self._positive_data = []
        self._negative_data = []
        # value
        self._best_solution = None

    def init_attribute(self):
        """
        Init self._data, self._positive_data, self._negative_data by sampling.

        :return: no return value
        """
        self._parameter.set_negative_size(self._parameter.get_train_size() - self._parameter.get_positive_size())
        # check if the initial solutions have been set
        data_temp = self._parameter.get_init_samples()
        i = 0
        iteration_num = self._parameter.get_train_size()
        if data_temp is not None and self._best_solution is None:
            size = len(data_temp)
            if iteration_num < size:
                size = iteration_num
            for j in range(size):
                if isinstance(data_temp[j], Solution) is False:
                    x = self._objective.construct_solution(data_temp[j])
                else:
                    x = data_temp[j]
                if math.isnan(x.get_value()):
                    self._objective.eval(x)
                self._data.append(x)
                ToolFunction.log("init solution %s, value: %s" % (i, x.get_value()))
                i += 1
        # otherwise generate random solutions

        while i < iteration_num:
            # distinct_flag: True means sample is distinct(can be use),
            # False means sample is distinct, you should sample again.
            x, distinct_flag = self.distinct_sample_from_set(self._objective.get_dim(), self._data,
                                                             data_num=iteration_num)
            # panic stop
            if x is None:
                break
            if distinct_flag:
                self._objective.eval(x)
                self._data.append(x)
                i += 1
        self.selection()
        return

    def selection(self):
        """
        This function sequentially does:
            Sort self._data
            Choose [first, train_size )solutions as the new self._data
            Choose first positive_size solutions as self._positive_data
            Choose [positive_size, train_size) solutions as self._negative_data

        :return: no return value
        """

        new_data = sorted(self._data, key=lambda x: x.get_value())
        self._data = new_data[0:self._parameter.get_train_size()]
        self._positive_data = new_data[0: self._parameter.get_positive_size()]
        self._negative_data = new_data[
            self._parameter.get_positive_size(): self._parameter.get_train_size()]
        self._best_solution = self._positive_data[0]
        return

    #
    def distinct_sample(self, dim, check_distinct=True, data_num=0):
        """
        Sample a distinct(compared with solutions in self._data) solution from dim.

        :param dim: a Dimension object
        :param check_distinct: whether to check the sampled solution is distinct
        :param data_num: the maximum number to sample
        :return: sampled solution and distinct_flag (True if it's distinct)
        """
        objective = self._objective
        x = objective.construct_solution(dim.rand_sample())
        times = 1
        distinct_flag = True
        if check_distinct is True:
            while self.is_distinct(self._positive_data, x) is False or \
                    self.is_distinct(self._negative_data, x) is False:
                x = objective.construct_solution(dim.rand_sample())
                times += 1
                if times % 10 == 0:
                    limited, number = dim.limited_space()
                    if limited is True:
                        if number <= data_num:
                            ToolFunction.log(
                                'racos_common.py: WARNING -- sample space has been fully enumerated. Stop early')
                            return None, None
                    if times > 100:
                        distinct_flag = False
                        break
        return x, distinct_flag

    def distinct_sample_from_set(self, dim, set, check_distinct=True, data_num=0):
        """
        Sample a distinct solution(compared with solutions in set) from dim.

        :param dim: a Dimension object
        :param set: a list containing other solutions
        :param check_distinct: whether to check the sampled solution is distinct
        :param data_num: the maximum number to sample
        :return: sampled solution and distinct_flag(True if distinct)
        """
        objective = self._objective
        x = objective.construct_solution(dim.rand_sample())
        times = 1
        distinct_flag = True
        if check_distinct is True:
            while self.is_distinct(set, x) is False:
                x = objective.construct_solution(dim.rand_sample())
                times += 1
                if times % 10 == 0:
                    limited, number = dim.limited_space()
                    if limited is True:
                        if number <= data_num:
                            ToolFunction.log(
                                'racos_common.py: WARNING -- sample space has been fully enumerated. Stop early')
                            return None, None
                    if times > 100:
                        distinct_flag = False
                        break
        return x, distinct_flag

    # Distinct sample from a classifier, return a solution
    # if check_distinct is False, you don't need to sample distinctly
    def distinct_sample_classifier(self, classifier, check_distinct=True, data_num=0):
        """
        Sample a distinct solution from a classifier.
        """

        x = classifier.rand_sample()
        ins = self._objective.construct_solution(x)
        times = 1
        distinct_flag = True
        if check_distinct is True:
            while self.is_distinct(self._positive_data, ins) is False or \
                    self.is_distinct(self._negative_data, ins) is False:
                x = classifier.rand_sample()
                ins = self._objective.construct_solution(x)
                times += 1
                if times % 10 == 0:
                    if times == 10:
                        space = classifier.get_sample_space()
                    limited, number = space.limited_space()
                    if limited is True:
                        if number <= data_num:
                            ToolFunction.log(
                                'racos_common: WARNING -- sample space has been fully enumerated. Stop early')
                            return None, None
                    if times > 100:
                        distinct_flag = False
                        break
        return ins, distinct_flag

    def show_best_solution(self, intermediate_print=False, times=0, freq=100):
        """
        Show intermediate best solutions every 'freq' evaluation.

        :param intermediate_print: whether to show
        :param times: current iteration time
        :param freq: frequency
        :return: no return value
        """
        if intermediate_print is True and times % freq == 0:
            ToolFunction.log(("budget %d, fx result: " % times) + str(self._best_solution.get_value()))
            ToolFunction.log("x: " + str(self._best_solution.get_x()))

    @staticmethod
    def extend(seta, setb):
        """
        Concatenate two list.
        """
        result = copy.deepcopy(seta)
        for x in setb:
            result.append(copy.deepcopy(x))
        return result

    @staticmethod
    def is_distinct(seta, x):
        """
        Check if x is distinct from each solution in seta.

        :param seta: a list
        :param x: a Solution object
        :return: True or False
        """
        for ins in seta:
            if x.is_equal(ins):
                return False
        return True

    def set_parameters(self, parameter):
        self._parameter = parameter
        return

    def get_parameters(self):
        return self._parameter

    def set_objective(self, objective):
        self._objective = objective
        return

    def get_objective(self):
        return self._objective

    # For debugging
    def print_positive_data(self):
        ToolFunction.log('------print positive_data------')
        ToolFunction.log('the size of positive_data is: %d' %
                         (len(self._positive_data)))
        for x in self._positive_data:
            x.print_solution()

    def print_negative_data(self):
        ToolFunction.log('------print negative_data------')
        ToolFunction.log('the size of negative_data is: %d' %
                         (len(self._negative_data)))
        for x in self._negative_data:
            x.print_solution()

    def print_data(self):
        ToolFunction.log('------print b------')
        ToolFunction.log('the size of b is: %d' % (len(self._data)))
        for x in self._data:
            x.print_solution()
