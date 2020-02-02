"""
This module contains the class RacosClassification, which provides a classifier for all Racos algorithms.

Author:
    Yu-Ren Liu
"""

from zoopt.dimension import Dimension
from zoopt.utils.tool_function import ToolFunction
import copy
import numpy as np


class RacosClassification:
    """
    This class implements a classifier used by all Racos algorithms.
    """

    def __init__(self, dim, positive, negative, ub=1):
        """
        Initialization

        :param dim: a Dimension object
        :param positive: positive population
        :param negative: negative population
        :param ub: uncertain bits, which is a parameter for Racos
        """
        self.__solution_space = dim
        self.__sample_region = []
        self.__label_index = []
        # Solution
        self.__positive_solution = positive
        self.__negative_solution = negative
        self.__x_positive = None
        self.__uncertain_bit = ub

        regions = dim.get_regions()
        for i in range(dim.get_size()):
            temp = [regions[i][0], regions[i][1]]
            self.__sample_region.append(temp)
        return

    def reset_classifier(self):
        """
        Reset this classifier.

        :return: no return value
        """
        regions = self.__solution_space.get_regions()
        for i in range(self.__solution_space.get_size()):
            self.__sample_region[i][0] = regions[i][0]
            self.__sample_region[i][1] = regions[i][1]
            self.__label_index = []
        self.__x_positive = None
        return

    # This algos always works, whether discrete or continuous, we always use this function.
    def mixed_classification(self):
        """
        The process to train this classifier, which can handle mixed search space(continuous and discrete).

        :return: no return value
        """

        self.__x_positive = self.__positive_solution[np.random.randint(
            0, len(self.__positive_solution))]
        len_negative = len(self.__negative_solution)
        index_set = list(range(self.__solution_space.get_size()))
        remain_index_set = list(range(self.__solution_space.get_size()))
        types = self.__solution_space.get_types()
        order = self.__solution_space.get_order()
        while len_negative > 0:
            if len(remain_index_set) == 0:
                ToolFunction.log('ERROR: sampled two same solutions, please raise issues on github')
            k = remain_index_set[np.random.randint(0, len(remain_index_set))]
            x_pos_k = self.__x_positive.get_x_index(k)
            # continuous
            if types[k] is True:
                x_negative = self.__negative_solution[
                    np.random.randint(0, len_negative)]
                x_neg_k = x_negative.get_x_index(k)
                if x_pos_k < x_neg_k:
                    r = np.random.uniform(x_pos_k, x_neg_k)
                    if r < self.__sample_region[k][1]:
                        self.__sample_region[k][1] = r
                        i = 0
                        while i < len_negative:
                            if self.__negative_solution[i].get_x_index(k) >= r:
                                len_negative -= 1
                                itemp = self.__negative_solution[i]
                                self.__negative_solution[i] = self.__negative_solution[len_negative]
                                self.__negative_solution[len_negative] = itemp
                            else:
                                i += 1
                else:
                    r = np.random.uniform(x_neg_k, x_pos_k)
                    if r > self.__sample_region[k][0]:
                        self.__sample_region[k][0] = r
                        i = 0
                        while i < len_negative:
                            if self.__negative_solution[i].get_x_index(k) <= r:
                                len_negative -= 1
                                itemp = self.__negative_solution[i]
                                self.__negative_solution[i] = self.__negative_solution[len_negative]
                                self.__negative_solution[len_negative] = itemp
                            else:
                                i += 1
            # discrete
            else:
                if order[k] is True:
                    x_negative = self.__negative_solution[
                        np.random.randint(0, len_negative)]
                    x_neg_k = x_negative.get_x_index(k)
                    if x_pos_k < x_neg_k:
                        # different from continuous version
                        r = np.random.randint(x_pos_k, x_neg_k)
                        if r < self.__sample_region[k][1]:
                            self.__sample_region[k][1] = r
                            i = 0
                            while i < len_negative:
                                if self.__negative_solution[i].get_x_index(k) >= r:
                                    len_negative -= 1
                                    itemp = self.__negative_solution[i]
                                    self.__negative_solution[i] = self.__negative_solution[len_negative]
                                    self.__negative_solution[len_negative] = itemp
                                else:
                                    i += 1
                    else:
                        r = np.random.randint(x_neg_k, x_pos_k + 1)
                        if r > self.__sample_region[k][0]:
                            self.__sample_region[k][0] = r
                            i = 0
                            while i < len_negative:
                                if self.__negative_solution[i].get_x_index(k) <= r:
                                    len_negative -= 1
                                    itemp = self.__negative_solution[i]
                                    self.__negative_solution[i] = self.__negative_solution[len_negative]
                                    self.__negative_solution[len_negative] = itemp
                                else:
                                    i += 1
                else:
                    delete = 0
                    i = 0
                    while i < len_negative:
                        if self.__negative_solution[i].get_x_index(k) != x_pos_k:
                            len_negative -= 1
                            delete += 1
                            itemp = self.__negative_solution[i]
                            self.__negative_solution[i] = self.__negative_solution[len_negative]
                            self.__negative_solution[len_negative] = itemp
                        else:
                            i += 1
                    remain_index_set.remove(k)
                    if delete != 0:
                        index_set.remove(k)
                    if len(index_set) == 0:
                        index_set.append(k)
        self.set_uncertain_bit(index_set)
        return

    def set_uncertain_bit(self, index_set):
        """
        Choose uncertain bits from iset.

        :param iset: index set
        :return: no return value
        """
        ub = min(self.__uncertain_bit, len(index_set))
        self.__label_index = np.random.choice(index_set, ub, replace=False)
        return

    def rand_sample(self):
        """
        Random sample from self.__solution_space.get_dim().

        :return: sampled x
        """
        x = copy.deepcopy(self.__x_positive.get_x())
        for index in self.__label_index:
            if self.__solution_space.get_type(index) is True:
                x[index] = np.random.uniform(self.__sample_region[index][0], self.__sample_region[index][1])
            else:
                x[index] = np.random.randint(self.__sample_region[index][0], self.__sample_region[index][1] + 1)
        return x

    def get_sample_region(self):
        return self.__sample_region

    def get_sample_space(self):
        size = self.__solution_space.get_size()
        regions = self.__sample_region
        types = self.__solution_space.get_types()
        return Dimension(size, regions, types)

    def get_positive_solution(self):
        return self.__positive_solution

    def get_negative_solution(self):
        return self.__negative_solution

    def get_x_positive(self):
        return self.__x_positive

    def get_label_index(self):
        return self.__label_index

    # for debugging
    def print_neg(self):
        """
        Print negative population.

        :return: no return value
        """
        ToolFunction.log('------print neg------')
        for x in self.__negative_solution:
            x.print_solution()

    def print_pos(self):
        """
        Print positive population.

        :return: no return value
        """

        ToolFunction.log('------print pos------')
        for x in self.__positive_solution:
            x.print_solution()

    def print_sample_region(self):
        """
        Print sample region.

        :return: no return value
        """
        ToolFunction.log('------print sample region------')
        ToolFunction.log(self.__sample_region)
