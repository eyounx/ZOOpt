
import numpy as np
from zoopt.utils.zoo_global import gl
from copy import deepcopy
import time
from zoopt.utils.tool_function import ToolFunction

"""
The canonical Pareto optimization
Running Pareto optimization will use the objective.eval_constraint function. This function makes the solution.get_value() a vector.
The first element of the vector is the objective function value by objective.__func, and the second element is the constraint degree by objective.__constraint

Author:
    Chao Feng, Yang Yu
"""

class ParetoOpt:

    def __init__(self):
        pass

    # every bit will be flipped with probability 1/n
    def mutation(self, s ,n):
        s_temp = deepcopy(s)
        threshold = 1.0 / n
        flipped = False
        for i in range(0,n):
            # the probability is 1/n
            if gl.rand.uniform(0,1) <= threshold:
                s_temp[0,i]=(s[0,i]+1)%2
                flipped = True
        if not flipped:
            mustflip = gl.rand.randint(0,n-1)
            s_temp[0, mustflip] = (s[0, mustflip] + 1) % 2

        return s_temp

    # This function is to find the index of s where element is 1
    def position(self,s):
        n=np.shape(s)[1]
        result=[]
        for i in range(0,n):
            if s[0,i]==1:
                result.append(i)
        return result   
            
    def opt(self, objective, parameter):
        evaluationFunc = objective.get_func()
        constraint = objective.get_constraint()
        isolationFunc = parameter.get_isolationFunc()
        n=objective.get_dim().get_size()

        # initiate the population
        sol = objective.construct_solution(np.zeros([1,n]))
        objective.eval_constraint(sol)

        population = [sol]
        fitness = [sol.get_value()]
        popSize = 1
        # iteration count
        t = 0
        T = parameter.get_budget()
        while t < T:
            if t == 0:
                time_log1 = time.time()
            # choose a individual from population randomly
            s = population[gl.rand.randint(1, popSize)-1]
            # every bit will be flipped with probability 1/n
            offSpringX = self.mutation(s.get_x(), n)
            offSpring = objective.construct_solution(offSpringX)
            objective.eval_constraint(offSpring)
            offSpringFit = offSpring.get_value()
            # now we need to update the population
            hasBetter = False

            for i in range(0, popSize):
                if isolationFunc(offSpringX)!=isolationFunc(population[i].get_x()):
                    continue
                else:
                    if (fitness[i][0] < offSpringFit[0] and fitness[i][1] >= offSpringFit[1]) or \
                            (fitness[i][0] <= offSpringFit[0] and fitness[i][1] > offSpringFit[1]):
                        hasBetter = True
                        break
            # there is no better individual than offSpring
            if not hasBetter:
                Q = []
                Qfit = []
                for j in range(0,popSize):
                    if offSpringFit[0] <= fitness[j][0] and offSpringFit[1] >= fitness[j][1]:
                        continue
                    else:
                        Q.append(population[j])
                        Qfit.append(fitness[j])
                Q.append(offSpring)
                Qfit.append(offSpringFit)
                # update fitness
                fitness=Qfit
                # update population
                population = Q
            t += 1
            popSize = np.shape(fitness)[0]

            # display expected running time
            if t == 5:
                time_log2 = time.time()
                expected_time = T * (time_log2 - time_log1) / 5
                if expected_time > 5:
                    m, s = divmod(expected_time, 60)
                    h, m = divmod(m, 60)
                    ToolFunction.log('expected remaining running time: %02d:%02d:%02d' % (h, m, s))

        resultIndex = -1
        maxValue=float('inf')
        for p in range(0, popSize):
            fitness = population[p].get_value()
            if fitness[1]>=0 and fitness[0] < maxValue:
                maxValue = fitness[0]
                resultIndex = p
        return population[resultIndex]


