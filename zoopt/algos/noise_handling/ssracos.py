#!/usr/bin/env python
# coding=utf-8

"""
This module contains the class SSRacos, which combines the noise handling method value suppression with SRacos.

Author:
    Xiong-Hui Chen, Yu-Ren Liu
"""

import time
from zoopt.algos.opt_algorithms.racos.racos_classification import RacosClassification
from zoopt.algos.opt_algorithms.racos.sracos import SRacos
from zoopt.utils.tool_function import ToolFunction
from zoopt.utils.zoo_global import gl


class SSRacos(SRacos):
    """
    This class implements SSRacos algorithm, which combines the noise handling method value suppression with SRacos.
    """

    def __init__(self):
        SRacos.__init__(self)
        return

    def opt(self, objective, parameter, strategy='WR', ub=1):
        """
        SSRacos optimization.

        :param objective: a Objective object
        :param parameter: a Parameter object
        :param strategy: replace strategy
        :param ub: uncertain bits, which is a parameter of SRacos
        :return: the best solution of the optimization
        """
        self.clear()
        self.set_objective(objective)
        self.set_parameters(parameter)
        self.init_attribute()
        self.i = 0
        iteration_num = self._parameter.get_budget() - self._parameter.get_train_size()
        time_log1 = time.time()
        max_distinct_repeat_times = 100
        current_not_distinct_times = 0
        last_best = None
        non_update_allowed = parameter.get_non_update_allowed()
        non_update_times = 0
        current_stay_times = 0
        non_update_baselines_times = 0

        while self.i < iteration_num:
            if gl.rand.random() < self._parameter.get_probability():
                classifier = RacosClassification(
                    self._objective.get_dim(), self._positive_data, self._negative_data, ub)
                classifier.mixed_classification()
                solution, distinct_flag = self.distinct_sample_classifier(
                    classifier, True, self._parameter.get_train_size())
            else:
                solution, distinct_flag = self.distinct_sample(
                    self._objective.get_dim())
            # panic stop
            if solution is None:
                ToolFunction.log(" [break loop] because solution is None")
                return self.get_best_solution()
            if distinct_flag is False:
                current_not_distinct_times += 1
                if current_not_distinct_times >= max_distinct_repeat_times:
                    ToolFunction.log(
                        "[break loop] because distinct_flag is false too much times")
                    return self.get_best_solution()
                else:
                    continue
            else:
                current_not_distinct_times = 0
            # evaluate the solution
            objective.eval(solution)
            # show best solution
            times = self.i + self._parameter.get_train_size() + 1
            self.show_best_solution(parameter.get_intermediate_result(), times,
                                    parameter.get_intermediate_freq())
            # suppression
            if self._is_worest(solution):
                non_update_times += 1
                if non_update_times >= non_update_allowed:
                    self._positive_data_re_sample()
                    self.update_possible_solution()
                    self._positive_data = self.sort_solution_list(
                        self._positive_data)
                    non_update_times = 0
                    best_solution = self.get_best_solution(for_test=True)
                    last_best = best_solution.get_resample_value()
            else:
                non_update_times = 0

            bad_ele = self.replace(self._positive_data, solution, 'pos')
            self.replace(self._negative_data, bad_ele, 'neg', strategy)
            self._best_solution = self._positive_data[0]

            if self.i == 4:
                time_log2 = time.time()
                expected_time = (self._parameter.get_budget(
                ) - self._parameter.get_train_size()) * (time_log2 - time_log1) / 5
                if self._parameter.get_time_budget() is not None:
                    expected_time = min(
                        expected_time, self._parameter.get_time_budget())
                if expected_time > 5:
                    m, s = divmod(expected_time, 60)
                    h, m = divmod(m, 60)
                    ToolFunction.log(
                        'expected remaining running time: %02d:%02d:%02d' % (h, m, s))
            # time budget check
            if self._parameter.get_time_budget() is not None:
                if (time.time() - time_log1) >= self._parameter.get_time_budget():
                    ToolFunction.log('time_budget runs out')
                    return self.get_best_solution()
            # terminal_value check
            if self._parameter.get_terminal_value() is not None:
                solution = self.get_best_solution(for_test=True)
                if solution is not None and solution.get_resample_value() <= self._parameter.get_terminal_value():
                    ToolFunction.log('terminal function value reached')
                    return self.get_best_solution()
            self.i += 1
        return self.get_best_solution()

    def update_possible_solution(self):
        """
        Search all of solutions in self._positive_data, add it to self._possible_solution_list if not exist.
        """
        for solution in self._positive_data:
            if solution.is_in_possible_solution:
                continue
            else:
                solution.is_in_possible_solution = True
                new_solution = solution.deep_copy()
                self._possible_solution_list.append(new_solution)

    def get_best_solution(self, for_test=False):
        """
        Find the best solution.

        :param for_test: if set for_test as False, this method will re-sample all of the solutions in positive data and then add them to possible solution before search the best solution.
        :return: return resample value if for_test is False otherwise return suppression value.
        """
        if not for_test:
            # update solution in positive data
            self._positive_data_re_sample()
            self.update_possible_solution()
        # sort
        sort_solution = self.sort_solution_list(
            self._possible_solution_list, key=lambda x: x.get_resample_value())
        if sort_solution == []:
            return None
        else:
            if not for_test:
                sort_solution[0].set_value(
                    sort_solution[0].get_resample_value())
                return sort_solution[0]
            else:
                return sort_solution[0]

    def sort_solution_list(self, solution_list, key=lambda x: x.get_value()):
        """
        Sort a solution list (eg. self._positive_data, self._possible_solution_list) with key

        :param solution_list: the solution list to be sorted.
        :param key: a function which input a solution and return its key.
        :return: return a copy of sorted list(without change origin solution list).
        """
        return sorted(solution_list, key=key)

    def _positive_data_re_sample(self):
        """
        Re-sample all of the solutions in positive data(ignore solutions which have re-sampled before).
        """
        for data in self._positive_data:
            iter_times = self._objective.resample(
                data, self.get_parameters().get_resample_times())
            self.i += iter_times

    def _is_worest(self, solution):
        """
        Judge if the solution is the worst solution in positive data.

        :param solution: the solution to be judged.
        :return: True if the solution is the worst False otherwise.
        """
        return self._positive_data[-1].get_value() <= solution.get_value()
