import theano
import theano.tensor as T
import numpy as np


class Layer(object):
    def __init__(self, in_size, out_size, activation_function=None):
        # w includes b, the last line of w is b
        self.__row = in_size + 1;
        self.__column = out_size;
        self.__w = theano.shared(np.random.normal(0, 1, (in_size + 1, out_size)))
        # self.b = theano.shared(np.zeros((out_size, )) + 0.1)
        self.__activation_function = activation_function
        self.__wx_plus_b = 0
        self.outputs = 0

    def output(self, inputs):
        self.__wx_plus_b = T.dot(inputs, self.__w) + self.b
        if self.__activation_function is None:
            self.outputs = self.__wx_plus_b
        else:
            self.outputs = self.__activation_function(self.__wx_plus_b)
        return self.outputs

    # The input x is a vector.This function decompose w into a matrix
    def decode_w(self, w):
        interval = self.__column
        begin = 0
        output = []
        step = len(w) / interval
        for i in range(step):
            output.append(w[begin: begin + interval])
            begin += interval
        self.__w = theano.shared(output)
        return output

    def set_w(self, w):
        self.__w = w
        return

    def get_row(self):
        return self.__row

    def get_column(self):
        return self.__column


class NNModel:
    def __init__(self):
        self.__layers = []
        self.__ws = []
        return

    def add_layer(self, layer):
        self.__layers.append(layer)
        return

    # This function decompose a vector into several vectors.
    def decode_w(self, w):
        # ws means a list of w
        ws = []
        begin = 0
        for i in range(len(self.__layers)):
            length = self.__layers[i].get_row() * self.__layers[i].get_column()
            ws.append(w[begin: begin + length])
            self.__layers[i].decode_w(ws[i])
        self.__ws = ws
        return ws

    # output y from input x
    def output(self, x):
        out = x
        for i in range(len(self.__layers)):
            out = self.__layers[i].output(out)
        return out




