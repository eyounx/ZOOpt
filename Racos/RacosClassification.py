"""
The class RacosClassification contains a classifier generation algorithm

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

from Dimension import Dimension
import Global
import sys
import Instance
import time
import copy


class RacosClassification:

    def __init__(self, dim, positive, negative, ub=1):
        self._solution_space = dim
        self._sample_region = []
        self._label = []
        # Instance
        self._positive_solution = positive
        self._negative_solution = negative
        self._x_positive = None
        self._uncertain_bit = ub

        regions = dim.get_regions()
        for i in range(dim.get_size()):
            temp = [regions[i][0], regions[i][1]]
            self._sample_region.append(temp)
            self._label.append(False)
        return

    def reset_classifier(self):
        regions = self._solution_space.get_regions()
        for i in range(self._solution_space.get_size()):
            self._sample_region[i][0] = regions[i][0]
            self._sample_region[i][1] = regions[i][1]
            self._label[i] = False
        self._x_positive = None

    # This method works if self._solution_space is discrete
    def discrete_classification(self):
        self._x_positive = self._positive_solution[Global.rand.randint(
            0, len(self._positive_solution) - 1)]
        len_negative = len(self._negative_solution)
        index_set = range(self._solution_space.get_size())
        while len_negative > 0:
            k = index_set[Global.rand.randint(0, len(index_set) - 1)]

            x_pos_k = self._x_positive.get_coordinate(k)
            i = 0
            delete = 0
            while i < len_negative:
                if self._negative_solution[i].get_coordinate(k) != x_pos_k:
                    len_negative -= 1
                    delete += 1
                    itemp = self._negative_solution[i]
                    self._negative_solution[i] = self._negative_solution[len_negative]
                    self._negative_solution[len_negative] = itemp
                else:
                        i += 1
            if delete != 0:
                index_set.remove(k)
        self.set_uncertain_bit(index_set)
        return

    # This method works if self._solution_space is continuous
    def continuous_classification(self):
        self._x_positive = self._positive_solution[Global.rand.randint(
            0, len(self._positive_solution) - 1)]
        len_negative = len(self._negative_solution)
        while len_negative > 0:
            k = Global.rand.randint(0, self._solution_space.get_size() - 1)
            x_negative = self._negative_solution[
                Global.rand.randint(0, len_negative - 1)]
            x_pos_k = self._x_positive.get_coordinate(k)
            x_neg_k = x_negative.get_coordinate(k)
            if x_pos_k < x_neg_k:
                r = Global.rand.uniform(x_pos_k, x_neg_k)
                if r < self._sample_region[k][1]:
                    self._sample_region[k][1] = r
                    i = 0
                    while i < len_negative:
                        if self._negative_solution[i].get_coordinate(k) >= r:
                            len_negative -= 1
                            itemp = self._negative_solution[i]
                            self._negative_solution[i] = self._negative_solution[len_negative]
                            self._negative_solution[len_negative] = itemp
                        else:
                            i += 1
            else:
                r = Global.rand.uniform(x_neg_k, x_pos_k)
                if r > self._sample_region[k][0]:
                    self._sample_region[k][0] = r
                    i = 0
                    while i < len_negative:
                        if self._negative_solution[i].get_coordinate(k) <= r:
                            len_negative -= 1
                            itemp = self._negative_solution[i]
                            self._negative_solution[i] = self._negative_solution[len_negative]
                            self._negative_solution[len_negative] = itemp
                        else:
                            i += 1
        index_set = range(self._solution_space.get_size())
        self.set_uncertain_bit(index_set)
        return

    # This method always works, whether discrete or continuous
    def mixed_classification(self):
        self._x_positive = self._positive_solution[Global.rand.randint(
            0, len(self._positive_solution) - 1)]
        len_negative = len(self._negative_solution)
        index_set = range(self._solution_space.get_size())
        types = self._solution_space.get_types()
        while len_negative > 0:
            k = index_set[Global.rand.randint(0, len(index_set) - 1)]
            x_pos_k = self._x_positive.get_coordinate(k)
            # continuous
            if types[k] is True:
                x_negative = self._negative_solution[
                    Global.rand.randint(0, len_negative - 1)]
                x_neg_k = x_negative.get_coordinate(k)
                if x_pos_k < x_neg_k:
                    r = Global.rand.uniform(x_pos_k, x_neg_k)
                    if r < self._sample_region[k][1]:
                        self._sample_region[k][1] = r
                        i = 0
                        while i < len_negative:
                            if self._negative_solution[i].get_coordinate(k) >= r:
                                len_negative -= 1
                                itemp = self._negative_solution[i]
                                self._negative_solution[i] = self._negative_solution[len_negative]
                                self._negative_solution[len_negative] = itemp
                            else:
                                i += 1
                else:
                    r = Global.rand.uniform(x_neg_k, x_pos_k)
                    if r > self._sample_region[k][0]:
                        self._sample_region[k][0] = r
                        i = 0
                        while i < len_negative:
                            if self._negative_solution[i].get_coordinate(k) <= r:
                                len_negative -= 1
                                itemp = self._negative_solution[i]
                                self._negative_solution[i] = self._negative_solution[len_negative]
                                self._negative_solution[len_negative] = itemp
                            else:
                                i += 1
            # discrete
            else:
                delete = 0
                i = 0
                while i < len_negative:
                    if self._negative_solution[i].get_coordinate(k) != x_pos_k:
                        len_negative -= 1
                        delete += 1
                        itemp = self._negative_solution[i]
                        self._negative_solution[i] = self._negative_solution[len_negative]
                        self._negative_solution[len_negative] = itemp
                    else:
                        i += 1
                if delete != 0:
                    index_set.remove(k)
        self.set_uncertain_bit(index_set)
        return

    # Choose uncertain bits from iset
    def set_uncertain_bit(self, iset):
        index_set = iset
        for i in range(self._uncertain_bit):
            index = index_set[Global.rand.randint(0, len(index_set) - 1)]
            self._label[index] = True
            index_set.remove(index)
        return

    # Random sample from self._solution_space.get_dim()
    def rand_sample(self):
        x = []
        for i in range(self._solution_space.get_size()):
            if self._label[i] is True:
                if self._solution_space.get_type(i) is True:
                    x.append(Global.rand.uniform(self._sample_region[i][0], self._sample_region[i][1]))
                else:
                    x.append(Global.rand.randint(self._sample_region[i][0], self._sample_region[i][1]))
            else:
                x.append(self._x_positive.get_coordinate(i))
        return x

    def get_sample_region(self):
        return self._sample_region

    def get_sample_space(self):
        size = self._solution_space.get_size()
        regions = self._sample_region
        types = self._solution_space.get_types()
        return Dimension(size, regions, types)

    # for debugging
    def print_neg(self):
        print '------print neg------'
        for x in self._negative_solution:
            x.print_instance()

    def print_pos(self):
        print '------print pos------'
        for x in self._positive_solution:
            x.print_instance()

    def print_sample_region(self):
        print '------print sample region------'
        print self._sample_region
