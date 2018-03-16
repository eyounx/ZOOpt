"""
This module contains the class PONSS, which is a variant of POSS to solve noisy subset selection problems.
"""
import time

import numpy as np

from zoopt.algos.opt_algorithms.paretoopt.paretoopt import ParetoOpt
from zoopt.utils.tool_function import ToolFunction
from zoopt.utils.zoo_global import gl


class PONSS(ParetoOpt):
    """
    This class implements PONSS algorithm, which is a variant of POSS to solve noisy subset selection problems.
    """

    def __init__(self):
        ParetoOpt.__init__(self)
        pass

    def opt(self, objective, parameter):
        """
        Pareto optimization under noise.

        :param objective: an Objective object
        :param parameter:  a Parameters object
        :return: the best solution of the optimization
        """
        isolationFunc = parameter.get_isolationFunc()
        theta = parameter.get_ponss_theta()
        b = parameter.get_ponss_b()
        n = objective.get_dim().get_size()

        # initiate the population
        sol = objective.construct_solution(np.zeros(n))
        objective.eval_constraint(sol)

        population = [sol]
        pop_size = 1
        # iteration count
        t = 0
        T = parameter.get_budget()
        while t < T:
            if t == 0:
                time_log1 = time.time()
            # choose a individual from population randomly
            s = population[gl.rand.randint(1, pop_size) - 1]
            # every bit will be flipped with probability 1/n
            offspring_x = self.mutation(s.get_x(), n)
            offspring = objective.construct_solution(offspring_x)
            objective.eval_constraint(offspring)
            offspring_fit = offspring.get_value()
            # now we need to update the population
            has_better = False

            for i in range(0, pop_size):
                if isolationFunc(offspring_x) != isolationFunc(population[i].get_x()):
                    continue
                else:
                    if self.theta_dominate(theta, population[i], offspring):
                        has_better = True
                        break
            # there is no better individual than offspring
            if not has_better:
                P = []
                Q = []
                for j in range(0, pop_size):
                    if self.theta_weak_dominate(theta, offspring, population[i]):
                        continue
                    else:
                        P.append(population[j])
                P.append(offspring)
                population = P
                for sol in population:
                    if sol.get_value()[1] == offspring.get_value()[1]:
                        Q.append(sol)
                if len(Q) == b + 1:
                    for sol in Q:
                        population.remove(sol)
                    j = 0
                    while j < b:
                        sols = gl.rand.sample(Q, 2)
                        Q.remove(sols[0])
                        Q.remove(sols[1])
                        objective.eval_constraint(sols[0])
                        objective.eval_constraint(sols[1])
                        if sols[0].get_value()[0] < sols[1].get_value()[0]:
                            population.append(sols[0])
                            Q.append(sols[1])
                        else:
                            population.append(sols[1])
                            Q.append(sols[0])
                        j += 1
                        t += 2
            t += 1
            pop_size = len(population)

            # display expected running time
            if t == 5:
                time_log2 = time.time()
                expected_time = T * (time_log2 - time_log1) / 5
                if expected_time > 5:
                    m, s = divmod(expected_time, 60)
                    h, m = divmod(m, 60)
                    ToolFunction.log('expected remaining running time: %02d:%02d:%02d' % (h, m, s))

        result_index = -1
        max_value = float('inf')
        for p in range(pop_size):
            fitness = population[p].get_value()
            if fitness[1] >= 0 and fitness[0] < max_value:
                max_value = fitness[0]
                result_index = p
        return population[result_index]

    @staticmethod
    def theta_dominate(theta, solution1, solution2):
        """
        Judge if solution1 theta dominates solution2.
        :param theta: threshold
        :param solution1: a Solution object
        :param solution2: a Solution object
        :return: True or False
        """
        fit1 = solution1.get_value()
        fit2 = solution2.get_value()
        if (fit1[0] + theta < fit2[0] and fit1[1] >= fit2[1]) or (fit1[0] + theta <= fit2[0] and fit1[1] > fit2[1]):
            return True
        else:
            return False

    @staticmethod
    def theta_weak_dominate(theta, solution1, solution2):
        """
        Judge if solution1 theta weakly dominates solution2.
        :param theta: threshold
        :param solution1: a Solution object
        :param solution2: a Solution object
        :return: True or False
        """
        fit1 = solution1.get_value()
        fit2 = solution2.get_value()
        if fit1[0] + theta <= fit2[0] and fit1[1] >= fit2[1]:
            return True
        else:
            return False
