"""
This module contains the implementation of Sparse MSE problem.

Author:
    Chao Feng
"""

import numpy as np
from zoopt import Opt, Parameter, Objective, Dimension, ExpOpt
import codecs
import arff


class SparseMSE:
    """
    This class implements the Sparse MSE problem.
    """
    _X = 0
    _Y = 0
    _C = 0
    _b = 0
    _size = 0
    _k = 0
    _best_solution = None

    def __init__(self, filename):
        """
        Initialization.
        :param filename: filename
        """
        data = self.read_data(filename)
        self._size = np.shape(data)[1] - 1
        self._X = data[:, 0: self._size]
        self._Y = data[:, self._size]
        self._C = self._X.T * self._X
        self._b = self._X.T * self._Y

    def position(self, s):
        """
        This function is to find the index of s where element is 1
        return a list of positions
        :param s:
        :return: a list of index of s where element is 1
        """
        n = len(s)
        result = []
        for i in range(n):
            if s[i] == 1:
                result.append(i)
        return result

    def constraint(self, solution):
        """
        If the constraints are satisfied, the constraint function will return a zero or positive value. Otherwise a
        negative value will be returned.

        :param solution: a Solution object
        :return: a zero or positive value which means constraints are satisfied, otherwise a negative value
        """
        x = solution.get_x()
        return self._k-sum(x)

    def set_sparsity(self, k):
        self._k = k

    def get_sparsity(self):
        return self._k

    def loss(self, solution):
        """
        loss function for sparse regression
        :param solution: a Solution object
        """
        x = solution.get_x()
        if sum(x) == 0.0 or sum(x) >= 2.0 * self._k:
            return float('inf')
        pos = self.position(x)
        alpha = (self._C[pos, :])[:, pos]
        alpha = alpha.I * self._b[pos, :]
        sub = self._Y - self._X[:, pos]*alpha
        mse = sub.T*sub / np.shape(self._Y)[0]
        return mse[0, 0]

    def get_dim(self):
        """
        Construct a Dimension object of this problem.
        :return: a dimension object of sparse mse.
        """
        dim_regs = [[0, 1]] * self._size
        dim_tys = [False] * self._size
        return Dimension(self._size, dim_regs, dim_tys)

    def read_data(self, filename):
        """
        Read data from file.
        :param filename: filename
        :return: normalized data
        """
        file_ = codecs.open(filename, 'rb', 'utf-8')
        decoder = arff.ArffDecoder()
        dataset = decoder.decode(file_.readlines(), encode_nominal=True)
        file_.close()
        data = dataset['data']
        return self.normalize_data(np.mat(data))

    @staticmethod
    def normalize_data(data_matrix):
        """
        Normalize data to have mean 0 and variance 1 for each column

        :param data_matrix: matrix of all data
        :return: normalized data
        """
        try:
            mat_size = np.shape(data_matrix)
            for i in range(0, mat_size[1]):
                the_column = data_matrix[:, i]
                column_mean = sum(the_column)/mat_size[0]
                minus_column = np.mat(the_column-column_mean)
                std = np.sqrt(np.transpose(minus_column)*minus_column/mat_size[0])
                data_matrix[:, i] = (the_column-column_mean)/std
            return data_matrix
        except Exception as e:
            print(e)
        finally:
            pass

    def get_k(self):
        return self._k
