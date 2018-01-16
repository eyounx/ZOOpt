"""
This module contains the class Racos, which is a optimization algorithm provided in ZOOpt.

Author:
    Yu-Ren Liu
"""

import time

from zoopt.algos.opt_algorithms.racos.racos_classification import RacosClassification
from zoopt.algos.opt_algorithms.racos.racos_common import RacosCommon
from zoopt.utils.tool_function import ToolFunction
from zoopt.utils.zoo_global import gl


class Racos(RacosCommon):
    """
    The class Racos represents Racos algorithm. It's inherited from RacosCommon.
    """

    def __init__(self):
        RacosCommon.__init__(self)

    def opt(self, objective, parameter, ub=1):
        """
        Racos optimization.

        :param objective: a Objective object
        :param parameter: a Parameter object
        :param ub: uncertain bits, which is a parameter of Racos
        :return: the best solution of the optimization
        """
        self.clear()
        self.set_objective(objective)
        self.set_parameters(parameter)
        self.init_attribute()
        t = self._parameter.get_budget() / self._parameter.get_negative_size()
        time_log1 = time.time()
        for i in range(t):
            j = 0
            iteration_num = len(self._negative_data)
            while j < iteration_num:
                if gl.rand.random() < self._parameter.get_probability():
                    classifier = RacosClassification(
                        self._objective.get_dim(), self._positive_data, self._negative_data, ub)
                    classifier.mixed_classification()
                    solution, distinct_flag = self.distinct_sample_classifier(classifier, True,
                                                                              self._parameter.get_train_size())
                else:
                    solution, distinct_flag = self.distinct_sample(self._objective.get_dim())
                # panic stop
                if solution is None:
                    return self._best_solution
                # If the solution had been sampled, skip it
                if distinct_flag is False:
                    continue
                # evaluate the solution
                objective.eval(solution)
                # show best solution
                times = i + self._parameter.get_train_size() + 1
                self.show_best_solution(parameter.get_intermediate_result(), times,
                                        parameter.get_intermediate_freq())
                self._data.append(solution)
                j += 1
            self.selection()
            self._best_solution = self._positive_data[0]
            # display expected running time
            if i == 4:
                time_log2 = time.time()
                expected_time = t * (time_log2 - time_log1) / 5
                if self._parameter.get_time_budget() is not None:
                    expected_time = min(expected_time, self._parameter.get_time_budget())
                if expected_time > 5:
                    m, s = divmod(expected_time, 60)
                    h, m = divmod(m, 60)
                    ToolFunction.log('expected remaining running time: %02d:%02d:%02d' % (h, m, s))
            # time budget check
            if self._parameter.get_time_budget() is not None:
                if time.time() - time_log1 >= self._parameter.get_time_budget:
                    ToolFunction.log('time_budget runs out')
                    return self._best_solution
            # terminal_value check
            if self._parameter.get_terminal_value() is not None:
                if self._best_solution.get_value() <= self._parameter.get_terminal_value():
                    ToolFunction.log('terminal function value reached')
                    return self._best_solution
        return self._best_solution
