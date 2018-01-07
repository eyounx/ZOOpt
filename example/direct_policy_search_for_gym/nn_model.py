"""
This file contains a class which defines a simple neural network model.

Author:
    Yu-Ren Liu
"""

import numpy as np
import math


class ActivationFunction:
    """
    This class defines activation functions in neural network.
    """
    @staticmethod
    # sigmoid function
    def sigmoid(x):
        """
        Sigmoid function.

        :param x: input of the sigmoid function
        :return: value of sigmoid(x)
        """
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
    """
    This class defines a layer in neural network.
    """

    def __init__(self, in_size, out_size, input_w=None, activation_function=None):
        """
        Init function.

        :param in_size: input size of this layer
        :param out_size: output size of this layer
        :param input_w: initial weight matrix
        :param activation_function: activation function of this layer
        """
        self.__row = in_size
        self.__column = out_size
        self.__w = []
        self.decode_w(input_w)
        self.__activation_function = activation_function
        self.__wx_plus_b = 0
        self.outputs = 0

    def cal_output(self, inputs):
        """
        Forward prop of one layer. In this example, we ignore bias.

        :param inputs: input of this layer
        :return:  output of this layer
        """

        self.__wx_plus_b = np.dot(inputs, self.__w)
        if self.__activation_function is None:
            self.outputs = self.__wx_plus_b
        else:
            self.outputs = self.__activation_function(self.__wx_plus_b)
        return self.outputs

    #
    def decode_w(self, w):
        """
        The input x is a vector and this function decompose w into a matrix.

        :param w: input weight vector
        :return: weight matrix
        """
        if w is None:
            return
        interval = self.__column
        begin = 0
        output = []
        step = int(len(w) / interval)
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
    """
        This class defines neural network.
    """
    def __init__(self):
        self.__layers = []
        self.__layer_size = []
        self.__w_size = 0
        return

    def construct_nnmodel(self, layers):
        """
        This function constructs a neural network from a list.

        :param layers:
            layers is a list, each element is the number of neurons in each layer
            len(layers) is at least 2, including input layer and output layer
        :return: no return value
        """
        self.__layer_size = layers
        for i in range(len(layers) - 1):
            self.add_layer(layers[i], layers[i + 1], activation_function=ActivationFunction.sigmoid)
            self.__w_size += layers[i] * layers[i + 1]

    def add_layer(self, in_size, out_size, input_w=None, activation_function=None):
        """
        Add one layer in neural network.

        :param in_size: input size of this layer
        :param out_size: output size of this layer
        :param input_w: initial weight matrix
        :param activation_function: activation function of this layer
        :return: no return value
        """
        new_layer = Layer(in_size, out_size, input_w, activation_function)
        self.__layers.append(new_layer)
        return

    #
    def decode_w(self, w):
        """
        This function decomposes a big vector into several vectors and assign them to weight matrices of the neural network.
        In the direct policy search example, big vector is the concatenation of all flattened weight matrices and small
        vectors are flattened weight matrices.

        :param w: concatenation of all flattened weight matrices
        :return: no return value
        """
        begin = 0
        for i in range(len(self.__layers)):
            length = self.__layers[i].get_row() * self.__layers[i].get_column()
            w_temp = w[begin: begin + length]
            self.__layers[i].decode_w(w_temp)
            begin += length
        return

    # output y from input x
    def cal_output(self, x):
        """
        Forward prop of the neural network.

        :param x: input of the neural network
        :return: output of the network
        """
        out = x
        for i in range(len(self.__layers)):
            out = self.__layers[i].cal_output(out)
        return out

    def get_w_size(self):
        return self.__w_size
