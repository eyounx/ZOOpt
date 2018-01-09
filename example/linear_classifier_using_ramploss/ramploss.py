"""
this example optimizes a linear classifier using the non-convex ramploss instead of any convex loss function.

this example requires the liac-arff package to read ARFF file

Author:
    Yu-Ren Liu, Yang Yu
"""

import arff, codecs
from zoopt import Dimension, Objective, Parameter, ExpOpt


class RampLoss:
    """
    Define ramploss learning loss function.
    """
    __data = None
    __test = None
    __ramploss_c = 10
    __ramploss_s = -1
    __dim_size = 0

    def __init__(self, arfffile):
        self.read_data(arfffile)

    def read_data(self, filename):
        """
        Read data from file.

        :param filename: Name of the file to read
        :return: no return
        """
        file_ = codecs.open(filename, 'rb', 'utf-8')
        decoder = arff.ArffDecoder()
        dataset = decoder.decode(file_.readlines(), encode_nominal=True)
        file_.close()
        self.__data = dataset['data']
        if self.__data is not None and self.__data[0] is not None:
            self.__dim_size = len(self.__data[0])

    def get_dim_size(self):
        return self.__dim_size

    def calc_product(self, weight, j):
        """
        Calculate product between the weights and the instance.

        :param weight: weight vector
        :param j: the index of the instance
        :return: product value
        """
        temp_sum = 0
        for i in range(len(weight) - 1):
            temp_sum += weight[i] * self.__data[j][i]
        temp_sum += weight[len(weight) - 1]
        return temp_sum

    def calc_h(self, ylfx, st):
        """
        Calculate hinge loss.
        """
        temp = st - ylfx
        if temp > 0:
            return temp
        else:
            return 0

    def calc_regularization(self, weight):
        """
        Calculate regularization
        """
        temp_sum = 0
        for i in range(len(weight)):
            temp_sum += weight[i] * weight[i]
        return temp_sum

    def trans_label(self, i):
        """
        Transform label from 0/1 to -1/+1
        """
        if self.__data[i][self.__dim_size - 1] == 1:
            return 1
        else:
            return -1

    #
    def eval(self, solution):
        """
        Objectve function to calculate the ramploss.
        """
        weight = solution.get_x()
        H1 = 0
        Hs = 0
        for i in range(len(self.__data)):
            fx = self.calc_product(weight, i)
            H1 += self.calc_h(self.trans_label(i) * fx, 1)
            Hs += self.calc_h(self.trans_label(i) * fx, self.__ramploss_s)
        regularization = self.calc_regularization(weight)
        value = regularization / 2 + self.__ramploss_c * H1 - self.__ramploss_c * Hs
        return value

    #
    def training_error(self, best):
        """
        Training error.
        """
        wrong = 0.0
        for i in range(len(self.__data)):
            fx = self.calc_product(best, i)
            if fx * self.trans_label(i) <= 0:
                wrong += 1
        rate = wrong / len(self.__data)
        return rate

    def dim(self):
        """
        Construct dimension of this problem.
        """
        return Dimension(self.__dim_size, [[-10, 10]] * self.__dim_size, [True] * self.__dim_size)


if __name__=='__main__':
    # read data
    loss = RampLoss('ionosphere.arff')
    objective = Objective(loss.eval, loss.dim())
    budget = 100 * loss.get_dim_size()
    parameter = Parameter(budget=budget)
    solution_list = ExpOpt.min(objective, parameter, repeat=1, plot=True, plot_file="img/ramploss.png")