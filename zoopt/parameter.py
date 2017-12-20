
import sys
import math
from zoopt.utils.tool_function import ToolFunction

"""
The class Parameter was implemented in this file.
A Parameter instance should be a necessary parameter to opt in RacosOptimization

Author:
    Yuren Liu, Yang Yu
"""


class Parameter:

    # Users should set at least algorithm and budget
    # algorithm can be 'racos' or 'poss'
    # If algorithm is 'racos' and sequential is True, opt will invoke SRacos.opt(default)
    # if algorithm is 'racos' and sequential is False, opt will invoke Racos.opt
    # budget cannot be None. It is the number of samples.
    # If autoset is True, train_size, positive_size, negative_size will be set automatically
    # If precision is None, we will set precision as 1e-17 in default. Otherwise, set precision
    # If uncertain_bits is None, racos will set uncertain_bits automatically
    # If init_samples is not None, the samples will be added into the first sampled solution set
    # If time_budget is not None, the algorithm should stop when the time_budget (in seconds)  runs out.
    # If terminal_value if not None, the algorithm should stop when such value is found
    # only if suppression is True, means use SSRACOS algorithm, non_update_allowed and resample_times are useful.
    # is found
    def __init__(self, algorithm=None, suppression=False, sequential=True, budget=0, intermediate_result=False,
                 intermediate_freq=100, intermediate_output=False, file_output="result.txt", autoset=True, precision=None,
                 uncertain_bits=None, init_samples=None, time_budget=None, terminal_value=None, non_update_allowed=40,
                 hot_start=False, save_racosc=False, file_racosc="file_racosc.txt", file_racosc_all="file_racosc_all.txt",
                 resample_times=100):
        self.__algorithm = algorithm
        self.__budget = budget

        # common parameters that all algorithm should accept
        self.__init_samples = init_samples
        self.__time_budget = time_budget
        self.__terminal_value = terminal_value

        ## for racos optimization
        self.__sequential = sequential
        self.__precision = precision
        self.__uncertain_bits = uncertain_bits
        self.__train_size = 0
        self.__positive_size = 0
        self.__negative_size = 0
        self.__probability = 0.99
        # for intermediate result
        self.__intermediate_result = intermediate_result
        tmp_freq = math.floor(intermediate_freq)
        self.__intermediate_freq = tmp_freq if tmp_freq >= 1 else 1
        self.__intermediate_output = intermediate_output
        self.__file_output = file_output

        self.__resample_times = resample_times
        self._suppression = suppression
        # temp
        self.__non_update_allowed = non_update_allowed

        # for hot start
        self.__hot_start = hot_start
        self.__save_racosc = save_racosc
        self.__file_racosc = file_racosc
        self.__file_racosc_all = file_racosc_all

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

    def get_suppressioin(self):
        return self._suppression

    def set_suppression(self, suppression):
        self._suppression = suppression

    def set_resample_times(self, resample_times):
        self.__resample_times = resample_times

    def get_resample_times(self):
        return self.__resample_times

    def set_non_update_allowed(self, non_update_allowed):
        self.__non_update_allowed = non_update_allowed

    def get_non_update_allowed(self):
        return self.__non_update_allowed

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

    def set_isolationFunc(self, func):
        self.__isolationFunc = func

    def get_isolationFunc(self):
        return self.__isolationFunc

    def set_init_samples(self, init_samples):
        self.__init_samples = init_samples

    def get_init_samples(self):
        return self.__init_samples

    def set_time_budget(self, time_budget):
        self.__time_budget = time_budget

    def get_time_budget(self):
        return self.__time_budget

    def set_terminal_value(self, terminal_value):
        self.__terminal_value = terminal_value

    def get_terminal_value(self):
        return self.__terminal_value

    def set_intermediate_result(self, intermediate_result):
        self.__intermediate_result = intermediate_result

    def get_intermediate_result(self):
        return self.__intermediate_result

    def get_intermediate_freq(self):
        return self.__intermediate_freq

# self.__hot_start = hot_start
#         self.__file_racosc = file_racosc
#         self.__file_racosc_all = file_racosc_all

    def get_hot_start(self):
        return self.__hot_start

    def get_save_racosc(self):
        return self.__save_racosc

    def get_file_racosc(self):
        return self.__file_racosc

    def get_file_racosc_all(self):
        return self.__file_racosc_all

