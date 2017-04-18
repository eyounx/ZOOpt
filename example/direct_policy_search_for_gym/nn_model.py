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
  LAMDA, http://lamda.nju.edu.cn
"""
import numpy as np

"""
define a simple neural network model.

Author:
    Yuren Liu
"""

class ActivationFunction:
    @staticmethod
    # sigmoid function
    def sigmoid(x):
        for i in range(len(x)):
            if -700 <= x[i] <= 700:
                x[i] = (2 / (1 + math.exp(-x[i]))) - 1  # sigmoid function
            else:
                if x[i] < -700:
                    x[i] = -1
                else:
                    x[i] = 1
        return x

class Layer(object):
    def __init__(self, in_size, out_size, input_w=None, activation_function=None):
        self.__row = in_size
        self.__column = out_size
        self.__w = []
        self.decode_w(input_w)
        self.__activation_function = activation_function
        self.__wx_plus_b = 0
        self.outputs = 0

    def cal_output(self, inputs):
        # In this example, we ignore bias
        self.__wx_plus_b = np.dot(inputs, self.__w)
        if self.__activation_function is None:
            self.outputs = self.__wx_plus_b
        else:
            self.outputs = self.__activation_function(self.__wx_plus_b)
        return self.outputs

    # The input x is a vector.This function decompose w into a matrix
    def decode_w(self, w):
        if w is None:
            return
        interval = self.__column
        begin = 0
        output = []
        step = len(w) / interval
        for i in range(step):
            output.append(w[begin: begin + interval])
            begin += interval
        self.__w = np.array(output)
        return

    def get_row(self):
        return self.__row

    def get_column(self):
        return self.__column


class NNModel:
    def __init__(self):
        self.__layers = []
        self.__layer_size = []
        self.__w_size = 0
        return

    # The input layers is a list, each element is the number of neurons in each layer.
    def construct_nnmodel(self, layers):
        # len(layers) is at least 2, including input layer and output layer
        self.__layer_size = layers
        for i in range(len(layers) - 1):
            self.add_layer(layers[i], layers[i + 1], activation_function=ActivationFunction.sigmoid)
            self.__w_size += layers[i] * layers[i + 1]

    def add_layer(self, in_size, out_size, input_w = None, activation_function=None):
        new_layer = Layer(in_size, out_size, input_w, activation_function)
        self.__layers.append(new_layer)
        return

    # This function decompose a vector into several vectors.
    def decode_w(self, w):
        # ws means a list of w
        begin = 0
        for i in range(len(self.__layers)):
            length = self.__layers[i].get_row() * self.__layers[i].get_column()
            w_temp = w[begin: begin + length]
            self.__layers[i].decode_w(w_temp)
            begin += length
        return

    # output y from input x
    def cal_output(self, x):
        out = x
        for i in range(len(self.__layers)):
            out = self.__layers[i].cal_output(out)
        return out

    def get_w_size(self):
        return self.__w_size


