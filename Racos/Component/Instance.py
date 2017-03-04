""""
The class Instance was implemented in this file.

Each sample like x from the dimension together with func(x) is an instance

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


class Instance:

    def __init__(self, coordinate=[], value=0):
        self.__coordinate = coordinate
        self.__value = value
        return

    # Deep copy this instance
    def deep_copy(self):
        coordinate = []
        for x in self.__coordinate:
            coordinate.append(x)
        value = self.__value
        return Instance(coordinate, value)

    # Check if two instances equal
    def judge_equal(self, ins, precision=1e-10):
        ins_coordinates = ins.get_coordinates()
        ins_value = ins.get_value()
        if abs(self.__value - ins_value) > precision:
            return False
        if len(self.__coordinate) != len(ins_coordinates):
            return False
        for i in range(len(self.__coordinate)):
            if abs(self.__coordinate[i] - ins_coordinates[i]) > precision:
                return False
        return True

    # Check if exists another instance in ins_set ths same as this one
    def exist_equal(self, ins_set):
        for ins in ins_set:
            if self.judge_equal(self, ins):
                return True
        return False

    def set_coordinate(self, index, coordinate):
        self.__coordinate[index] = coordinate
        return

    def set_coordinates(self, coordinate):
        self.__coordinate = coordinate
        return

    def set_value(self, value):
        self.__value = value
        return

    def get_coordinate(self, index):
        return self.__coordinate[index]

    def get_coordinates(self):
        return self.__coordinate

    def get_value(self):
        return self.__value

    def print_instance(self):
        print 'coordinates are: ' + repr(self.__coordinate)
        print 'value is ' + repr(self.__value)

    # Deep copy an instance set
    @staticmethod
    def deep_copy_set(ins_set):
        result_set = []
        for ins in ins_set:
            result_set.append(ins.deep_copy())
        return result_set

    # print the value of each instance in an instance set
    @staticmethod
    def print_instance_set(ins_set):
        for ins in ins_set:
            print 'value is %f' % (ins.get_value())
        return

    # Find the maximum instance of the iset
    @staticmethod
    def find_maximum(iset):
        maxi = float('-Inf')
        max_index = 0
        for i in range(len(iset)):
            if iset[i].get_value() > maxi:
                maxi = iset[i].get_value()
                max_index = i
        return iset[max_index], max_index

    # Find the minimum instance of the iset
    @staticmethod
    def find_minimum(iset):
        mini = float('Inf')
        mini_index = 0
        for i in range(len(iset)):
            if iset[i].get_value() < mini:
                mini = iset[i].get_value()
                mini_index = i
        return mini, mini_index



