"""
This module contains the class Dimension, which describes the dimension information of the search space.

Author:
    Yu-Ren Liu
"""

from zoopt.utils.zoo_global import gl
from zoopt.utils.tool_function import ToolFunction
import copy


class Dimension:
    """
    This class describes the dimension information of the search space.
    """

    def __init__(self, size=0, regs=[], tys=[], order=[]):
        """
        Initialization.

        :param size: dimension size
        :param regs: search space of each dimension
        :param tys: continuous or discrete for each dimension
        :param order:
            this parameter matters if this dimension is discrete, it means this dimension has partial order relation
        """
        self._size = size
        self._regions = regs
        # True means continuous, False means discrete
        self._types = tys
        if len(order) == 0:
            self._order = [False] * self._size
        else:
            self._order = order
        return


    @staticmethod
    def judge_match(size, regs, tys):
        """
        Check if the size of regs and tys are both the same as self._size.

        :return: True or False
        """
        if size != len(regs) or size != len(tys):
            ToolFunction.log('dimension.py: dimensions do not match')
            return False
        else:
            return True

    @staticmethod
    def merge_dim(dim1, dim2):
        """
        Merge two Dimension object.

        :return: a new merged Dimension object
        """
        res_dim = copy.deepcopy(dim1)
        res_dim.set_size(dim1.get_size() + dim2.get_size())
        res_dim.get_regions().extend(dim2.get_regions())
        res_dim.get_types().extend(dim2.get_types())
        res_dim.get_order().extend(dim2.get_order())
        return res_dim

    def equal(self, dim2):
        if self._size == dim2.get_size() and self._regions == dim2.get_regions() and self._types == dim2.get_types() \
                and self._order == dim2.get_order():
            return True
        else:
            return False

    def set_all(self, size, regs, tys):
        """
        Set all attributes

        :return: no return value
        """
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
            ToolFunction.log('dimension.py: index out of bound')
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

    def rand_sample(self):
        """
        Random sample in the search space.

        :return: a sampled x
        """
        x = []
        for i in range(self._size):
            if self._types[i] is True:
                value = gl.rand.uniform(
                    self._regions[i][0], self._regions[i][1])
            else:
                value = gl.rand.randint(self._regions[i][0], self._regions[i][1])
            x.append(value)
        return x

    def limited_space(self):
        """
        Judge if the dimension described search space is limited.

        :return:
            return True and the number of dimension value if each dimension is discrete.
            Otherwise, return False and zero
        """
        number = 1
        for i in range(self._size):
            if self._types[i] is True:
                return False, 0
            else:
                number *= self._regions[i][1] - self._regions[i][0] + 1
        return True, number

    def deep_copy(self):
        """
        Deep copy this instance.

        :return: a new instance
        """
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

    def copy_region(self):
        """
        Deep copy the instance's search regions.

        :return: a new search region
        """
        regions = []
        for reg in self._regions:
            interval = []
            for i in range(len(reg)):
                interval.append(reg[i])
            regions.append(interval)
        return regions

    def is_discrete(self):
        """
        Whether the search space of all dimensions is discrete.

        :return: True or False
        """
        for i in range(len(self._types)):
            if self._types[i] is True:
                return False
        return True

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

    def get_order(self):
        return self._order

    def set_size(self, size):
        self._size = size

    def set_order(self, order):
        self._order = order

    # for debugging
    def print_dim(self):
        """
        Print the dimension information.
        :return: no return value
        """
        ToolFunction.log('dim size: %d' % self._size)
        ToolFunction.log('dim regions is:')
        ToolFunction.log(self._regions)
        ToolFunction.log('dim types is:')
        ToolFunction.log(self._types)
