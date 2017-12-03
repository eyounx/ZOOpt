
from zoopt.utils.zoo_global import gl
from zoopt.utils.tool_function import ToolFunction
"""
The class Dimension was implemented in this file.

This class describes dimension messages.

Author:
    Yuren Liu
"""


class Dimension:

    def __init__(self, size=0, regs=[], tys=[], include_upper_bound=False):
        self._size = size
        self._regions = regs
        # True means continuous, False means discrete
        self._types = tys
        self.include_upper_bound = include_upper_bound
        return

    # Check if the dimensions of regs and tys
    # are both the same as size
    @staticmethod
    def judge_match(size, regs, tys):
        if size != len(regs) or size != len(tys):
            ToolFunction.log('dimension.py: dimensions do not match')
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

    # random sample from dimension messages.
    # this algos returns a list.
    def rand_sample(self):
        x = []
        for i in range(self._size):
            if self._types[i] is True:
                if not self.include_upper_bound:
                    value = gl.rand.uniform(
                        self._regions[i][0], self._regions[i][1])
                else:
                    value = gl.rand.uniform(
                        self._regions[i][0], self._regions[i][1]+gl.precision * 2)
            else:
                rand_index = gl.rand.randint(0, len(self._regions[i]) - 1)
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

    def is_discrete(self):
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

    # for debugging
    def print_dim(self):
        ToolFunction.log('dim size: %d' % self._size)
        ToolFunction.log('dim regions is:')
        ToolFunction.log(self._regions)
        ToolFunction.log('dim types is:')
        ToolFunction.log(self._types)
