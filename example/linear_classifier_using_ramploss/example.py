""""
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
  LAMDA, http://lamda.nju.edu.cn
"""
import arff, codecs
from zoo.dimension import Dimension
from zoo.objective import Objective
from zoo.parameter import Parameter
from zoo.opt import Opt

"""
this example optimizes a linear classifier using the non-convex ramploss instead of any convex loss function.

this example requires the liac-arff package to read ARFF file

Author:
    Yuren Liu, Yang Yu
"""


## define ramploss learning loss function
class RampLoss:
    __data = None
    __test = None
    __ramploss_c = 10
    __ramploss_s = -1
    __dim_size = 0

    def __init__(self, arfffile):
        self.read_data(arfffile)

    # Read data from file
    def read_data(self, filename):
        file_ = codecs.open(filename, 'rb', 'utf-8')
        decoder = arff.ArffDecoder()
        dataset = decoder.decode(file_.readlines(), encode_nominal=True)
        file_.close()
        self.__data = dataset['data']
        if( self.__data is not None and self.__data[0] is not None):
            self.__dim_size = len(self.__data[0])

    def get_dim_size(self):
        return self.__dim_size

    # calculate product between the weights and the instance
    def calc_product(self, weight, j):
        temp_sum = 0
        for i in range(len(weight) - 1):
            temp_sum += weight[i] * self.__data[j][i]
        temp_sum += weight[len(weight) - 1]
        return temp_sum

    # calculate hinge loss
    def calc_h(self, ylfx, st):
        temp = st - ylfx
        if temp > 0:
            return temp
        else:
            return 0

    # calculate norm
    def calc_norm(self, weight):
        temp_sum = 0
        for i in range(len(weight)):
            temp_sum += weight[i] * weight[i]
        return temp_sum

    # transform label from 0/1 to -1/+1
    def trans_label(self, i):
        if self.__data[i][self.__dim_size - 1] == 1:
            return 1
        else:
            return -1

    # calculate the ramploss
    def eval(self, solution):
        weight = solution.get_x()
        H1 = 0
        Hs = 0
        for i in range(len(self.__data)):
            fx = self.calc_product(weight, i)
            H1 += self.calc_h(self.trans_label(i) * fx, 1)
            Hs += self.calc_h(self.trans_label(i) * fx, self.__ramploss_s)
        norm = self.calc_norm(weight)
        value = norm / 2 + self.__ramploss_c * H1 - self.__ramploss_c * Hs
        return value

    # training error
    def trainerror(self, best):
        wrong = 0.0
        for i in range(len(self.__data)):
            fx = self.calc_product(best, i)
            if fx * self.trans_label(i) <= 0:
                wrong += 1
        rate = wrong / len(self.__data)
        return rate

    def dim(self):
        return Dimension( self.__dim_size, [[-10, 10]] * self.__dim_size, [True] * self.__dim_size)


if __name__=='__main__':
    # read data
    loss = RampLoss('ionosphere.arff')
    # optimization
    repeat = 5
    result = []
    for i in range(repeat):

        objective = Objective(loss.eval, loss.dim())
        budget = 100 * loss.get_dim_size()
        parameter = Parameter(budget=budget)
        # perform optimization
        ins = Opt.min(objective, parameter)

        print 'Best solution is:'
        ins.print_solution()
        print 'training error:', loss.trainerror(ins.get_x())