"""
This module contains the class Dimension, which describes the dimension information of the search space.

Author:
    Yu-Ren Liu

Updated by:
    Ze-Wen Li
"""

from zoopt.utils.zoo_global import gl
from zoopt.utils.tool_function import ToolFunction
import numpy as np
import copy


class Dimension(object):
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
                value = np.random.uniform(
                    self._regions[i][0], self._regions[i][1])
            else:
                value = np.random.randint(self._regions[i][0], self._regions[i][1]+1)
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


class ValueType(enumerate):
    CONTINUOUS = 1
    DISCRETE = 0


class Dimension2(object):
    """
    This class describes the dimension information of the search space.
    `Dimension2` has the same function as `Dimension` class, but the format of parameters is different.
    """

    def __init__(self, dim_list=[]):
        """
        Initialization.

        :param dim_list: a list of dimensions
                    for continuous dimension: (type, range, float_precision)
                                        e.g.: (ValueType.CONTINUOUS, [0, 1], 1e-6)
                    for discrete dimension: (type, range, has_partial_order)
                                        e.g.: (ValueType.DISCRETE, [0, 1], False)

        """
        gl.float_precisions = []
        self._size = len(dim_list)
        self._regions = list(map(lambda x: x[1], dim_list))
        # True means continuous, False means discrete
        self._types = list(map(lambda x: x[0] == True, dim_list))
        self._order_or_precision = list(map(lambda x: x[2], dim_list))

        for _dim in dim_list:
            if _dim[0] == ValueType.CONTINUOUS:
                _str_x = str(_dim[2])
                _precision_len = None
                if _dim[2] == 1:
                    _precision_len = 0
                elif _dim[2] > 1:
                    if 'e+' in _str_x:
                        _precision_len = 0 - int(_str_x.split('e+')[-1])
                    else:
                        _precision_len = 1 - len(str(int(_dim[2])))
                else:
                    assert _dim[2] != 0, "input float_precision must not be 0!"
                    if 'e-' in _str_x:
                        _precision_len = int(_str_x.split('e-')[-1])
                    elif '.' in _str_x:
                        _precision_len = len(_str_x.split('.')[-1])
                    else:
                        ToolFunction.log('sample wrong, input float_precision is invalid!')

                gl.float_precisions.append(_precision_len)
            else:
                gl.float_precisions.append(None)

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
        Merge two Dimension2 object.

        :return: a new merged Dimension2 object
        """
        res_dim = copy.deepcopy(dim1)
        res_dim.set_size(dim1.get_size() + dim2.get_size())
        res_dim.get_regions().extend(dim2.get_regions())
        res_dim.get_types().extend(dim2.get_types())
        res_dim.get_order_or_precision().extend(dim2.get_order_or_precision())
        return res_dim

    def equal(self, dim2):
        if self._size == dim2.get_size() and self._regions == dim2.get_regions() and self._types == dim2.get_types() \
                and self._order_or_precision == dim2.get_order_or_precision():
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
            if self._types[i]:
                value = round(np.random.uniform(self._regions[i][0], self._regions[i][1]), gl.float_precisions[i])
            else:
                value = np.random.randint(self._regions[i][0], self._regions[i][1] + 1)
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
            if self._types[i]:
                return False, 0
            else:
                number *= self._regions[i][1] - self._regions[i][0] + 1
        return True, number

    def deep_copy(self):
        """
        Deep copy this instance.

        :return: a new instance
        """
        regions = []
        tys = []
        order_or_precision = []
        for reg in self._regions:
            interval = []
            for i in range(len(reg)):
                interval.append(reg[i])
            regions.append(interval)
        for x in self._types:
            tys.append(x)
        for y in self._order_or_precision:
            order_or_precision.append(y)

        dim_li = []
        for i in range(len(tys)):
            dim_li.append((tys[i], regions[i], order_or_precision[i]))
        return Dimension2(dim_li)

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
            if self._types[i]:
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

    def get_order_or_precision(self):
        return self._order_or_precision

    def set_size(self, size):
        self._size = size

    def set_order_or_precision(self, order_or_precision):
        self._order_or_precision = order_or_precision

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