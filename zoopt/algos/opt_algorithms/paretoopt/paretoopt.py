"""
The canonical Pareto optimization
Running Pareto optimization will use the objective.eval_constraint function. This function makes the solution.get_value() a vector.
The first element of the vector is the objective function value by objective.__func, and the second element is the constraint degree by objective.__constraint

Author:
    Chao Feng, Yang Yu
"""

import numpy as np
from zoopt.utils.zoo_global import gl
from copy import deepcopy
import time
from zoopt.utils.tool_function import ToolFunction


class ParetoOpt:

    """
    Pareto optimization.
    """
    def __init__(self):
        pass

    @staticmethod
    def mutation(s, n):
        """
        Every bit of s will be flipped with probability 1/n.

        :param s: s is a list
        :param n: the probability of flipping is set to 1/n
        :return: flipped s
        """
        s_temp = deepcopy(s)
        threshold = 1.0 / n
        flipped = False
        for i in range(0, n):
            # the probability is 1/n
            if gl.rand.uniform(0, 1) <= threshold:
                s_temp[i] = (s[i] + 1) % 2
                flipped = True
        if not flipped:
            mustflip = gl.rand.randint(0, n-1)
            s_temp[mustflip] = (s[mustflip] + 1) % 2
        return s_temp

    def opt(self, objective, parameter):
        """
        Pareto optimization.

        :param objective: an Objective object
        :param parameter: a Parameters object
        :return: the best solution of the optimization
        """
        isolationFunc = parameter.get_isolationFunc()
        n = objective.get_dim().get_size()

        # initiate the population
        sol = objective.construct_solution(np.zeros(n))
        objective.eval_constraint(sol)

        population = [sol]
        fitness = [sol.get_value()]
        pop_size = 1
        # iteration count
        t = 0
        T = parameter.get_budget()
        while t < T:
            if t == 0:
                time_log1 = time.time()
            # choose a individual from population randomly
            s = population[gl.rand.randint(1, pop_size)-1]
            # every bit will be flipped with probability 1/n
            offspring_x = self.mutation(s.get_x(), n)
            offspring = objective.construct_solution(offspring_x)
            objective.eval_constraint(offspring)
            offspring_fit = offspring.get_value()
            # now we need to update the population
            hasBetter = False

            for i in range(0, pop_size):
                if isolationFunc(offspring_x) != isolationFunc(population[i].get_x()):
                    continue
                else:
                    if (fitness[i][0] < offspring_fit[0] and fitness[i][1] >= offspring_fit[1]) or \
                            (fitness[i][0] <= offspring_fit[0] and fitness[i][1] > offspring_fit[1]):
                        hasBetter = True
                        break
            # there is no better individual than offspring
            if not hasBetter:
                Q = []
                Qfit = []
                for j in range(0, pop_size):
                    if offspring_fit[0] <= fitness[j][0] and offspring_fit[1] >= fitness[j][1]:
                        continue
                    else:
                        Q.append(population[j])
                        Qfit.append(fitness[j])
                Q.append(offspring)
                Qfit.append(offspring_fit)
                # update fitness
                fitness=Qfit
                # update population
                population = Q
            t += 1
            pop_size = np.shape(fitness)[0]

            # display expected running time
            if t == 5:
                time_log2 = time.time()
                expected_time = T * (time_log2 - time_log1) / 5
                if expected_time > 5:
                    m, s = divmod(expected_time, 60)
                    h, m = divmod(m, 60)
                    ToolFunction.log('expected remaining running time: %02d:%02d:%02d' % (h, m, s))
        result_index = -1
        max_value=float('inf')
        for p in range(0, pop_size):
            fitness = population[p].get_value()
            if fitness[1] >= 0 and fitness[0] < max_value:
                max_value = fitness[0]
                result_index = p
        return population[result_index]


