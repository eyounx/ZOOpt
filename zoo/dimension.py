""""
The class Dimension was implemented in this file.

This class describes dimension messages.

Author:
    Yu-Ren Liu

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

import zoo.utils.my_global


class Dimension:

    def __init__(self, size=0, regs=[], tys=[]):
        self._size = size
        self._regions = regs
        self._types = tys
        return

    # Check if the dimensions of regs and tys
    # are both the same as size
    @staticmethod
    def judge_match(self, size, regs, tys):
        if size != len(regs) or size != len(tys):
            print 'dimensions don\'t match '
            return False
        else:
            return True

    # Set all the attributes
    def set_all(self, size, regs, tys):
        if self.judge_match(size, regs, tys) is False:
            return
        self._size = size
        self._regions = regs
        self._types = tys
        return

    def set_dimension_size(self, size):
        self._size = size
        return

    def set_region(self, index, reg, ty):
        if index > self._size - 1:
            print 'index out of bound'
            return
        self._regions[index] = reg
        self._types[index] = ty
        return

    def set_regions(self, regs, tys):
        if self.judge_match(self._size, regs, tys) is False:
            return
        self._regions = regs
        self._types = tys
        return

    # random sample from dimension messages.
    # this algos returns a list.
    def rand_sample(self):
        x = []
        for i in range(self._size):
            if self._types[i] is True:
                value = zoo.utils.my_global.rand.uniform(
                    self._regions[i][0], self._regions[i][1])
            else:
                rand_index = zoo.utils.my_global.rand.randint(0, len(self._regions[i]) - 1)
                value = self._regions[i][rand_index]
            x.append(value)
        return x

    # This algos will return True and the number of dimension value if each dimension is discrete.
    # Otherwise, return False and zero
    def limited_space(self):
        number = 1
        for i in range(self._size):
            if self._types[i] is True:
                return False, 0
            else:
                number *= self._regions[i][1] - self._regions[i][0] + 1
        return True, number

    # deep copy this instance
    def deep_copy(self):
        size = self._size
        regions = []
        tys = []
        for reg in self._regions:
            interval = []
            for i in range(len(reg)):
                interval.append(reg[i])
            regions.append(interval)
        for x in self._types:
            tys.append(x)
        return Dimension(size, regions, tys)

    # deep copy the instance's regions information
    def copy_region(self):
        regions = []
        for reg in self._regions:
            interval = []
            for i in range(len(reg)):
                interval.append(reg[i])
            regions.append(interval)
        return regions

    def get_size(self):
        return self._size

    def get_region(self, index):
        return self._regions[index]

    def get_regions(self):
        return self._regions

    def get_type(self, index):
        return self._types[index]

    def get_types(self):
        return self._types

    # for debugging
    def print_dim(self):
        print 'dim size is: %d' % self._size
        print 'dim regions is:'
        print self._regions
        print 'dim types is:'
        print self._types
