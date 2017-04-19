
import sys
from zoopt.utils.tool_function import ToolFunction

"""
The class Parameter was implemented in this file.
A Parameter instance should be a necessary parameter to opt in RacosOptimization

Author:
    Yuren Liu
"""


class Parameter:

    # Users should set at least algorithm and budget
    # algorithm can be 'racos' or 'poss'
    # If algorithm is 'racos' and sequential is True, opt will invoke SRacos.opt(default)
    # if algorithm is 'racos' and sequential is False, opt will invoke Racos.opt
    # If autoset is True, train_size, positive_size, negative_size will be set automatically
    # If precision is None, we will set precision as 1e-17 in default. Otherwise, set precision
    # If uncertain_bits is None, racos will set uncertain_bits automatically
    def __init__(self, algorithm=None, sequential=True, budget=0, autoset=True, precision=None, uncertain_bits=None):
        self.__algorithm = algorithm
        self.__budget = budget

        # for racos optimization
        self.__sequential = sequential
        self.__precision = precision
        self.__uncertain_bits = uncertain_bits
        self.__train_size = 0
        self.__positive_size = 0
        self.__negative_size = 0
        self.__probability = 0.99

        # for pareto optimization
        self.__isolationFunc = lambda x: 0

        if budget != 0 and autoset is True:
            self.auto_set(budget)
        return

    # Set train_size, positive_size, negative_size by following rules:
    # budget < 3 ->> error
    # budget: 4-50 ->> train_size = 4, positive_size = 1
    # budget: 51-100 ->> train_size = 6, positive_size = 1
    # budget: 101-1000 ->> train_size = 12, positive_size = 2
    # budget > 1001 ->> train_size = 22, positive_size = 2
    def auto_set(self, budget):
        if budget < 3:
            ToolFunction.log('parameter.py: budget too small')
            sys.exit(1)
        elif budget <= 50:
            self.__train_size = 4
            self.__positive_size = 1
        elif budget <= 100:
            self.__train_size = 6
            self.__positive_size = 1
        elif budget <= 1000:
            self.__train_size = 12
            self.__positive_size = 2
        else:
            self.__train_size = 22
            self.__positive_size = 2
        self.__negative_size = self.__train_size - self.__positive_size

    def set_algorithm(self, algorithm):
        self.__algorithm = algorithm

    def get_algorithm(self):
        return self.__algorithm

    def set_sequential(self, sequential):
        self.__sequential = sequential
        return

    def get_sequential(self):
        return self.__sequential

    def set_budget(self, budget):
        self.__budget = budget
        return

    def get_budget(self):
        return self.__budget

    def set_precision(self, precision):
        self.__precision = precision
        return

    def get_precision(self):
        return self.__precision

    def set_uncertain_bits(self, uncertain_bits):
        self.__uncertain_bits = uncertain_bits
        return

    def get_uncertain_bits(self):
        return self.__uncertain_bits

    def set_train_size(self, size):
        self.__train_size = size
        return

    def get_train_size(self):
        return self.__train_size

    def set_positive_size(self, size):
        self.__positive_size = size
        return

    def get_positive_size(self):
        return self.__positive_size

    def set_negative_size(self, size):
        self.__negative_size = size
        return

    def get_negative_size(self):
        return self.__negative_size

    def set_probability(self, probability):
        self.__probability = probability

    def get_probability(self):
        return self.__probability

    def set_isolationFunc(self,func):
        self.__isolationFunc=func

    def get_isolationFunc(self):
        return self.__isolationFunc









