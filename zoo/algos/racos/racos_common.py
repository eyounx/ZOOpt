"""
The class RacosC(means RacosCommon) contains common attributes and methods between Racos and SRacos.
Class Racos and SRacos both inherit from RacosC.

Author:
    Yu-Ren Liu

Time:
    2017.1.20
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

 Copyright (C) 2015 Nanjing University, Nanjing, China
 """

import copy
import sys


class RacosCommon:

    def __init__(self):
        self._parameter = None
        # Instance set
        # Random sampled Instances construct self._data
        self._data = []
        # self._positive_data are best-positive_size instance set
        self._positive_data = []
        # self._negative_data are the others
        self._negative_data = []
        # Instance
        self._best_solution = None
        return

    def clear(self):
        self._parameter = None
        # Instance
        self._data = []
        self._positive_data = []
        self._negative_data = []
        # value
        self._best_solution = None

    def set_parameters(self, parameter):
        self._parameter = parameter
        self.init_attribute()
        return

    # Construct self._data, self._positive_data, self._negative_data
    def init_attribute(self):
        for i in range(self._parameter.get_train_size()):
            x = self.distinct_sample(self._parameter.get_objective().get_dim())
            self._data.append(x)
        self.selection()
        return

    # Sort self._data
    # Choose first-train_size instances as the new self._data
    # Choose first-positive_size instances as self._positive_data
    # Choose [positive_size, train_size](Include the begin, not include the end) instances as self._negative_data
    def selection(self):
        new_data = sorted(self._data, key=lambda x: x.get_value())
        self._data = new_data[0:self._parameter.get_train_size()]
        self._positive_data = new_data[0: self._parameter.get_positive_size()]
        self._negative_data = new_data[self._parameter.get_positive_size(): self._parameter.get_train_size()]
        self._best_solution = self._positive_data[0]
        return

    @staticmethod
    def extend(seta, setb):
        result = copy.deepcopy(seta)
        for x in setb:
            result.append(copy.deepcopy(x))
        return result

    # Check if x is distinct from each instance in seta
    # return False if there exists an instance the same as x,
    # otherwise return True
    @staticmethod
    def judge_distinct(seta, x):
        for ins in seta:
            if x.judge_equal(ins):
                return False
        return True

    # Distinct sample from dim, return an instance
    def distinct_sample(self, dim, turnon=True, data_num=0):
        objective = self._parameter.get_objective()
        x = objective.construct_instance(dim.rand_sample())
        times = 1
        if turnon is True:
            while self.judge_distinct(self._positive_data, x) is False and \
                    self.judge_distinct(self._negative_data, x) is False:
                # print '------sample repeated------'
                x = objective.construct_instance(dim.rand_sample())
                times += 1
                if times % 10 == 0:
                    limited, number = dim.limited_space()
                    if limited is True:
                        if number <= data_num:
                            print '------data number in sample space is too small------'
                            sys.exit()
                    # if times > 100:
                    #     print '------error dead repeated------'
                    #     sys.exit()
        return x

    def distinct_sample_classifier(self, classifier, turnon=True, data_num=0):
        x = classifier.rand_sample()
        ins = self._parameter.get_objective().construct_instance(x)
        times = 1
        if turnon is True:
            while self.judge_distinct(self._positive_data, ins) is False or \
                    self.judge_distinct(self._negative_data, ins) is False:
                    # print '------sample repeated------'
                x = classifier.rand_sample()
                ins = self._parameter.get_objective().construct_instance(x)
                times += 1
                if times % 10 == 0:
                    if times == 10:
                        space = classifier.get_sample_space()
                    limited, number = space.limited_space()
                    if limited is True:
                        if number <= data_num:
                            print '------data number in sample space is too small------'
                            sys.exit()
                    if times > 100:
                        print '------error dead repeated------'
                        classifier.get_sample_space().print_dim()
                        sys.exit()
        return ins

    # For debugging
    def print_positive_data(self):
        print '------print positive_data------'
        print 'the size of positive_data is: %d' % (len(self._positive_data))
        for x in self._positive_data:
            x.print_instance()

    def print_negative_data(self):
        print '------print negative_data------'
        print 'the size of negative_data is: %d' % (len(self._negative_data))
        for x in self._negative_data:
            x.print_instance()

    def print_data(self):
        print '------print b------'
        print 'the size of b is: %d' % (len(self._data))
        for x in self._data:
            x.print_instance()
