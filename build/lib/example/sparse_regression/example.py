
import numpy as np
from zoopt.opt import Opt
from zoopt.parameter import Parameter
from zoopt.objective import Objective
from zoopt.dimension import Dimension
from math import exp
import codecs
import arff

"""
Objective functions can be implemented in this file

Author:
    Chao Feng
"""

class Sparse_MSE:
    _X = 0
    _Y = 0
    _C = 0
    _b = 0
    _size = 0
    _k = 0
    _best_solution = None

    def __init__(self, filename):
        data = self.read_data(filename)
        self._size = np.shape(data)[1] - 1
        self._X = data[:, 0: self._size]
        self._Y = data[:, self._size]
        self._C = self._X.T * self._X
        self._b = self._X.T * self._Y

    def position(self,s):
        n=np.shape(s)[1]
        result=[]
        for i in range(0,n):
            if s[0,i]==1:
                result.append(i)
        return result

    # constraint function returns a zero or positive value mean constraints are satisfied, otherwise negative
    def constraint(self,solution):
        x = solution.get_x()
        return self._k-x[0,:].sum()

    def set_sparsity(self, k):
        self._k = k

    def get_sparsity(self):
        return self._k
     
    def loss(self,solution):
        x = solution.get_x()
        if x[0, :].sum()==0.0 or x[0, :].sum()>=2.0*self._k:
            return float('inf')
        pos = self.position(x)
        alpha = (self._C[pos, :])[:, pos]
        alpha = alpha.I * self._b[pos, :]
        sub = self._Y - self._X[:, pos]*alpha
        mse= sub.T*sub / np.shape(self._Y)[0]
        return mse[0,0]

    def get_dim(self):
        dim_regs = [[0, 1]] * self._size
        dim_tys = [False] * self._size
        return Dimension(self._size, dim_regs, dim_tys)

    # Read data from file
    def read_data(self, filename):
        file_ = codecs.open(filename, 'rb', 'utf-8')
        decoder = arff.ArffDecoder()
        dataset = decoder.decode(file_.readlines(), encode_nominal=True)
        file_.close()
        data = dataset['data']
        return self.normlize_data(np.mat(data))

    #normalize data to have mean 0 and variance 1 for each column
    def normlize_data(self, dataMatrix):
        try:
            matSize=np.shape(dataMatrix)
            for i in range(0,matSize[1]):
                theColum=dataMatrix[:,i]
                columnMean=sum(theColum)/matSize[0]
                minusColumn=np.mat(theColum-columnMean)
                std=np.sqrt(np.transpose(minusColumn)*minusColumn/matSize[0])
                dataMatrix[:,i]=(theColum-columnMean)/std
            return dataMatrix
        except  Exception as e:
            print  e
        finally:
            pass


if __name__=='__main__':
    # load data file
    mse = Sparse_MSE('sonar.arff')
    mse.set_sparsity(8)

    # setup objective
    objective = Objective(func=mse.loss, dim=mse.get_dim(), constraint=mse.constraint)
    parameter = Parameter(algorithm='poss', budget=2 * exp(1) * mse.get_sparsity() * mse.get_sparsity() * mse.get_dim().get_size())

    # perform sparse regression with constraint |w|_0 <= k
    result = Opt.min(objective, parameter)
    print('the best solution is:', np.array(result.get_x())[0].tolist())
    print('with objective value:', result.get_value()[0], 'and sparsity:', result.get_value()[1] + mse.get_sparsity())
