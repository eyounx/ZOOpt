"""
The class Racos represents Racos algorithm. It's inherited from RacosC.

Author:
    Yuren Liu

"""

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

import time

from zoo.algos.racos.racos_classification import RacosClassification
from zoo.algos.racos.racos_common import RacosCommon
from zoo.utils import my_global


class Racos(RacosCommon):

    def __init__(self):
        RacosCommon.__init__(self)

    # racos optimization function
    def opt(self, objective, parameter, ub=1):
        self.clear()
        self.set_objective(objective)
        self.set_parameters(parameter)
        self.init_attribute()
        t = self._parameter.get_budget() / self._parameter.get_negative_size()
        for i in range(t):
            if i == 0:
                time_log1 = time.time()
            j = 0
            iteration_num = len(self._negative_data)
            while j < iteration_num:
                if my_global.rand.random() < self._parameter.get_probability():
                    classifier = RacosClassification(
                        self._objective.get_dim(), self._positive_data, self._negative_data, ub)
                    classifier.mixed_classification()
                    solution, distinct_flag = self.distinct_sample_classifier(classifier, True,
                                                                              self._parameter.get_train_size())
                else:
                    solution, distinct_flag = self.distinct_sample(self._objective.get_dim())
                # If the solution had been sampled, skip it
                if distinct_flag is False:
                    continue
                self._data.append(solution)
                j += 1
            self.selection()
            self._best_solution = self._positive_data[0]
            if i == 4:
                time_log2 = time.time()
                expected_time = t * (time_log2 - time_log1) / 5
                if expected_time > 5:
                    m, s = divmod(expected_time, 60)
                    h, m = divmod(m, 60)
                    print 'expected running time will be %02d:%02d:%02d' % (h, m, s)
        return self._best_solution

