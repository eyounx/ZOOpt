"""
This module contains the class SRacos, which is the sequential version of Racos (a classification based optimization algorithm).

Author:
    Yu-ren Liu
"""

import time
import numpy as np
from multiprocessing import Process, Queue

from zoopt.algos.opt_algorithms.racos.racos_classification import RacosClassification
from zoopt.algos.opt_algorithms.racos.sracos import SRacos
from zoopt.utils.tool_function import ToolFunction


class ASRacos():
    def __init__(self):
        self.asracoscont = ASRacosCont()

    def opt(self, objective, parameter, strategy='WR', ub=1):
        """
        SRacos optimization.

        :param objective: an Objective object
        :param parameter: a Parameter object
        :param strategy: replace strategy
        :param ub: uncertain bits, which is a parameter of SRacos
        :return: Optimization result
        """
        self.asracoscont.clear()
        self.asracoscont.set_objective(objective)
        self.asracoscont.set_parameters(parameter)
        unevaluated_queue = Queue()
        evaluated_queue = Queue()
        result_queue = Queue()
        history_queue = Queue()
        for i in range(parameter.server_num):
            evaluator = Evaluator(objective, i, unevaluated_queue, evaluated_queue)
            evaluator.start()
        self.asracoscont.parallel_init_attribute(unevaluated_queue, evaluated_queue)
        updater = Updater(objective, parameter, unevaluated_queue, evaluated_queue, result_queue, history_queue, self.asracoscont,
                          strategy, ub)
        updater.start()
        result = result_queue.get(block=True, timeout=None)
        self.asracoscont.get_objective().set_history(history_queue.get(block=True, timeout=None))
        return result


class ASRacosCont(SRacos):
    """
    The class SRacos represents Sequential Racos algorithm. It's inherited from RacosCommon.
    """

    def __init__(self):
        """
        Initialization.
        """
        SRacos.__init__(self)
        return


class Evaluator(Process):
    def __init__(self, objective, number, unevaluated_queue, evaluated_queue):
        super(Evaluator, self).__init__()
        self.objective = objective
        self.number = number
        self.unevaluated_queue = unevaluated_queue
        self.evaluated_queue = evaluated_queue
        self.daemon = True

    def run(self):
        while True:
            sol = self.unevaluated_queue.get(block=True, timeout=None)
            self.objective.eval(sol)
            # print('process ' + str(self.number) + " value: " + str(sol.get_value()))
            self.evaluated_queue.put(sol, block=True, timeout=None)


class Updater(Process):
    def __init__(self, objective, parameter, unevaluated_queue, evaluated_queue, result_queue, history_queue, asracoscont, strategy='WR', ub=1):
        super(Updater, self).__init__()
        self.objective = objective
        self.parameter = parameter
        self.asracoscont = asracoscont
        self.unevaluated_queue = unevaluated_queue
        self.evaluated_queue = evaluated_queue
        self.result_queue = result_queue
        self.history_queue = history_queue
        self.strategy = strategy
        self.ub = ub
        self.daemon = True
        if parameter.get_seed() is not None:
            np.random.seed(parameter.get_seed() + 2)

    def run(self):
        stopping_criterion = self.parameter.get_stopping_criterion()
        i = 0
        iteration_num = self.parameter.get_budget() - self.parameter.get_train_size()

        time_log1 = time.time()
        max_distinct_repeat_times = 100
        under_evaluate_list = []
        classifier = RacosClassification(
            self.objective.get_dim(), self.asracoscont.get_positive_data(), self.asracoscont.get_negative_data(), self.ub)
        classifier.mixed_classification()
        t = 0
        history = []
        sampled_data = self.asracoscont.get_positive_data() + self.asracoscont.get_negative_data()
        while t < self.parameter.server_num:
            solution, distinct_flag = self.asracoscont.distinct_sample_classifier(classifier, sampled_data, True,
                                                                       self.parameter.get_train_size())
            if distinct_flag is False:
                ToolFunction.log(
                    "[break initiation] cannot sample non-repetitive solutions from the search space.")
                self.result_queue.put(self.asracoscont.get_best_solution(), block=True, timeout=None)
                return
            solution.set_no(t)
            under_evaluate_list.append(solution)
            sampled_data.append(solution)
            self.unevaluated_queue.put(solution, block=True, timeout=None)
            t += 1
        while i < iteration_num:
            # evaluate the solution
            assert len(under_evaluate_list) == self.parameter.server_num
            new_sol = self.evaluated_queue.get(block=True, timeout=None)
            history.append(self.asracoscont.get_best_solution().get_value())
            # show best solution
            times = i + self.parameter.get_train_size() + 1
            self.asracoscont.show_best_solution(self.parameter.get_intermediate_result(), times, self.parameter.get_intermediate_freq())
            bad_ele = self.asracoscont.replace(self.asracoscont.get_positive_data(), new_sol, 'pos')
            self.asracoscont.replace(self.asracoscont.get_negative_data(), bad_ele, 'neg', self.strategy)
            self.asracoscont.set_best_solution(self.asracoscont.get_positive_data()[0])
            if i == 4:
                time_log2 = time.time()
                expected_time = (self.parameter.get_budget() - self.parameter.get_train_size()) * \
                                (time_log2 - time_log1) / 5
                if self.parameter.get_time_budget() is not None:
                    expected_time = min(
                        expected_time, self.parameter.get_time_budget())
                if expected_time > 5:
                    m, s = divmod(expected_time, 60)
                    h, m = divmod(m, 60)
                    ToolFunction.log(
                        'expected remaining running time: %02d:%02d:%02d' % (h, m, s))
            # time budget check
            if self.parameter.get_time_budget() is not None:
                if (time.time() - time_log1) >= self.parameter.get_time_budget():
                    ToolFunction.log('time_budget runs out')
                    self.result_queue.put(self.asracoscont.get_best_solution(), block=True, timeout=None)
                    return
            # terminal_value check
            if self.parameter.get_terminal_value() is not None:
                if self.asracoscont.get_best_solution().get_value() <= self.parameter.get_terminal_value():
                    ToolFunction.log('the terminal function value is reached')
                    self.result_queue.put(self.asracoscont.get_best_solution(), block=True, timeout=None)
                    return
            if stopping_criterion.check(self) is True:
                self.result_queue.put(self.asracoscont.get_best_solution(), block=True, timeout=None)
                return
            i += 1
            current_not_distinct_times = 0
            solution = None
            sampled_data = self.asracoscont.get_positive_data() + self.asracoscont.get_negative_data() + under_evaluate_list
            while current_not_distinct_times < max_distinct_repeat_times:
                if np.random.rand() < self.parameter.get_probability():
                    classifier = RacosClassification(
                        self.objective.get_dim(), self.asracoscont.get_positive_data(), self.asracoscont.get_negative_data(), self.ub)
                    classifier.mixed_classification()
                    solution, distinct_flag = self.asracoscont.distinct_sample_classifier(
                        classifier, sampled_data, True, self.parameter.get_train_size())
                else:
                    solution, distinct_flag = self.asracoscont.distinct_sample(
                        self.objective.get_dim(), sampled_data)
                # panic stop
                if solution is None:
                    ToolFunction.log(" [break loop] failure in sampling new solutions")
                    self.result_queue.put(self.asracoscont.get_best_solution(), block=True, timeout=None)
                    return
                if distinct_flag is True:
                    break
                current_not_distinct_times += 1
            solution.set_no(new_sol.get_no())
            if current_not_distinct_times >= max_distinct_repeat_times:
                ToolFunction.log(
                    "[break loop] cannot sample non-repetitive solutions from the search space.")
                self.objective.set_history(history)
                self.result_queue.put(self.asracoscont.get_best_solution(), block=True, timeout=None)
                self.history_queue.put(history, block=True, timeout=None)
                return
            under_evaluate_list[new_sol.get_no()] = solution
            self.unevaluated_queue.put(solution, block=True, timeout=None)
        self.objective.set_history(history)
        self.result_queue.put(self.asracoscont.get_best_solution(), block=True, timeout=None)
        self.history_queue.put(history, block=True, timeout=None)
        return
