"""
The class RacosClassification contains a classifier generation algorithm

Author:
    Yuren Liu

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

from zoo.dimension import Dimension

from zoo.utils.zoo_global import gl


class RacosClassification:

    def __init__(self, dim, positive, negative, ub=1):
        self.__solution_space = dim
        self.__sample_region = []
        self.__label = []
        # Solution
        self.__positive_solution = positive
        self.__negative_solution = negative
        self.__x_positive = None
        self.__uncertain_bit = ub

        regions = dim.get_regions()
        for i in range(dim.get_size()):
            temp = [regions[i][0], regions[i][1]]
            self.__sample_region.append(temp)
            self.__label.append(False)
        return

    def reset_classifier(self):
        regions = self.__solution_space.get_regions()
        for i in range(self.__solution_space.get_size()):
            self.__sample_region[i][0] = regions[i][0]
            self.__sample_region[i][1] = regions[i][1]
            self.__label[i] = False
        self.__x_positive = None
        return

    # This algos always works, whether discrete or continuous, we always use this function.
    def mixed_classification(self):
        self.__x_positive = self.__positive_solution[gl.rand.randint(
            0, len(self.__positive_solution) - 1)]
        len_negative = len(self.__negative_solution)
        index_set = range(self.__solution_space.get_size())
        types = self.__solution_space.get_types()
        while len_negative > 0:
            k = index_set[gl.rand.randint(0, len(index_set) - 1)]
            x_pos_k = self.__x_positive.get_x_index(k)
            # continuous
            if types[k] is True:
                x_negative = self.__negative_solution[
                    gl.rand.randint(0, len_negative - 1)]
                x_neg_k = x_negative.get_x_index(k)
                if x_pos_k < x_neg_k:
                    r = gl.rand.uniform(x_pos_k, x_neg_k)
                    if r < self.__sample_region[k][1]:
                        self.__sample_region[k][1] = r
                        i = 0
                        while i < len_negative:
                            if self.__negative_solution[i].get_x_index(k) >= r:
                                len_negative -= 1
                                itemp = self.__negative_solution[i]
                                self.__negative_solution[i] = self.__negative_solution[len_negative]
                                self.__negative_solution[len_negative] = itemp
                            else:
                                i += 1
                else:
                    r = gl.rand.uniform(x_neg_k, x_pos_k)
                    if r > self.__sample_region[k][0]:
                        self.__sample_region[k][0] = r
                        i = 0
                        while i < len_negative:
                            if self.__negative_solution[i].get_x_index(k) <= r:
                                len_negative -= 1
                                itemp = self.__negative_solution[i]
                                self.__negative_solution[i] = self.__negative_solution[len_negative]
                                self.__negative_solution[len_negative] = itemp
                            else:
                                i += 1
            # discrete
            else:
                delete = 0
                i = 0
                while i < len_negative:
                    if self.__negative_solution[i].get_x_index(k) != x_pos_k:
                        len_negative -= 1
                        delete += 1
                        itemp = self.__negative_solution[i]
                        self.__negative_solution[i] = self.__negative_solution[len_negative]
                        self.__negative_solution[len_negative] = itemp
                    else:
                        i += 1
                if delete != 0:
                    index_set.remove(k)
        self.set_uncertain_bit(index_set)
        return

    # Choose uncertain bits from iset
    def set_uncertain_bit(self, iset):
        index_set = iset
        for i in range(self.__uncertain_bit):
            index = index_set[gl.rand.randint(0, len(index_set) - 1)]
            self.__label[index] = True
            index_set.remove(index)
        return

    # Random sample from self.__solution_space.get_dim()
    def rand_sample(self):
        x = []
        for i in range(self.__solution_space.get_size()):
            if self.__label[i] is True:
                if self.__solution_space.get_type(i) is True:
                    x.append(gl.rand.uniform(self.__sample_region[i][0], self.__sample_region[i][1]))
                else:
                    x.append(gl.rand.randint(self.__sample_region[i][0], self.__sample_region[i][1]))
            else:
                x.append(self.__x_positive.get_x_index(i))
        return x

    def get_sample_region(self):
        return self.__sample_region

    def get_sample_space(self):
        size = self.__solution_space.get_size()
        regions = self.__sample_region
        types = self.__solution_space.get_types()
        return Dimension(size, regions, types)

    def get_positive_solution(self):
        return self.__positive_solution

    def get_negative_solution(self):
        return self.__negative_solution

    def get_x_positive(self):
        return self.__x_positive

    def get_label(self):
        return self.__label

    # for debugging
    def print_neg(self):
        print '------print neg------'
        for x in self.__negative_solution:
            x.print_solution()

    def print_pos(self):
        print '------print pos------'
        for x in self.__positive_solution:
            x.print_solution()

    def print_sample_region(self):
        print '------print sample region------'
        print self.__sample_region
