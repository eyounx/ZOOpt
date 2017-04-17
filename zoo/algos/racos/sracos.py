"""
 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 as published by the Free Software Foundation; either version 2
 of the License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

 Copyright (C) 2017 Nanjing University, Nanjing, China
"""

"""
The class SRacos represents SRacos algorithm. It's inherited from RacosCommon.

Author:
    Yuren Liu
"""

import time
import numpy
from zoo.solution import Solution
from zoo.algos.racos.racos_classification import RacosClassification
from zoo.algos.racos.racos_common import RacosCommon
from zoo.utils.zoo_global import gl


class SRacos(RacosCommon):
    def __init__(self):
        RacosCommon.__init__(self)
        return

    # SRacos's optimization function
    # Default strategy is WR(worst replace)
    # Default uncertain_bits is 1, but actually ub will be set either by user or by RacosOptimization automatically.
    def opt(self, objective, parameter, strategy='WR', ub=1):
        self.clear()
        self.set_objective(objective)
        self.set_parameters(parameter)
        self.init_attribute()
        i = 0
        iteration_num = self._parameter.get_budget() - self._parameter.get_train_size()
        while i < iteration_num:
            if i == 0:
                time_log1 = time.time()
            if gl.rand.random() < self._parameter.get_probability():
                classifier = RacosClassification(
                    self._objective.get_dim(), self._positive_data, self._negative_data, ub)
                classifier.mixed_classification()
                ins, distinct_flag = self.distinct_sample_classifier(classifier, True, self._parameter.get_train_size())
            else:
                ins, distinct_flag = self.distinct_sample(self._objective.get_dim())
            if distinct_flag is False:
                continue
            # evaluate the solution
            objective.eval(ins)
            bad_ele = self.replace(self._positive_data, ins, 'pos')
            self.replace(self._negative_data, bad_ele, 'neg', strategy)
            self._best_solution = self._positive_data[0]
            if i == 4:
                time_log2 = time.time()
                expected_time = (self._parameter.get_budget() - self._parameter.get_train_size()) * \
                                (time_log2 - time_log1) / 5
                if expected_time > 5:
                    m, s = divmod(expected_time, 60)
                    h, m = divmod(m, 60)
                    print 'expected running time will be %02d:%02d:%02d' % (h, m, s)
            i += 1
        return self._best_solution

    def replace(self, iset, x, iset_type, strategy='WR'):
        if strategy == 'WR':
            return self.strategy_wr(iset, x, iset_type)
        elif strategy == 'RR':
            return self.strategy_rr(iset, x)
        elif strategy == 'LM':
            best_sol = min(iset, key=lambda x: x.get_value())
            return self.strategy_lm(iset, best_sol, x)

    # Find first element larger than x
    def binary_search(self, iset, x, begin, end):
        x_value = x.get_value()
        if x_value <= iset[begin].get_value():
            return begin
        if x_value >= iset[end].get_value():
            return end + 1
        if end == begin + 1:
            return end
        mid = (begin + end) // 2
        if x_value <= iset[mid].get_value():
            return self.binary_search(iset, x, begin, mid)
        else:
            return self.binary_search(iset, x, mid, end)

    # Worst replace
    def strategy_wr(self, iset, x, iset_type):
        if iset_type == 'pos':
            index = self.binary_search(iset, x, 0, len(iset) - 1)
            iset.insert(index, x)
            worst_ele = iset.pop()
        else:
            worst_ele, worst_index = Solution.find_maximum(iset)
            if worst_ele.get_value() > x.get_value():
                iset[worst_index] = x
            else:
                worst_ele = x
        return worst_ele

    # Random replace
    def strategy_rr(self, iset, x):
        len_iset = len(iset)
        replace_index = gl.rand.randint(0, len_iset - 1)
        replace_ele = iset[replace_index]
        iset[replace_index] = x
        return replace_ele

    # replace the farthest solution from best_sol
    def strategy_lm(self, iset, best_sol, x):
        farthest_dis = 0
        farthest_index = 0
        for i in range(iset):
            dis = self.distance(iset[i].get_coordinates(), best_sol.get_coordinates())
            if dis > farthest_dis:
                farthest_dis = dis
                farthest_index = i
        farthest_ele = iset[farthest_index]
        iset[farthest_index] = x
        return farthest_ele

    @staticmethod
    def distance(x, y):
        dis = 0
        for i in range(len(x)):
            dis += (x[i] - y[i])**2
        return numpy.sqrt(dis)
