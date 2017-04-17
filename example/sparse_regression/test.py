import numpy as np
from zoo.algos.paretoopt.NormalizeData import NormlizeDate
from zoo.opt import Opt
from zoo.parameter import Parameter
from zoo.objective import Objective
import numpy as np
from zoo.dimension import Dimension


class MSE:
    def __init__(self,X,y):
        self._best_solution = None
        self._X=X
        self._y=y
        self._C=X.T*X
        self._b=X.T*y
        self._size=np.shape(X)
        
    def position(self,s):
        n=np.shape(s)[1]
        result=[]
        for i in range(0,n):
            if s[0,i]==1:
                result.append(i)
        return result  
      
    def Loss(self,solution):
        pos = self.position(solution)
        alpha = (self._C[pos, :])[:, pos].I*self._b[pos, :]
        sub = self._y - self._X[:, pos]*alpha
        mse=sub.T*sub/self._size[0]
        return mse

if __name__=='__main__':
    #get normalized data from file 
    orginX=NormlizeDate("housing.txt")
    n=np.shape(orginX)[1]
    X=orginX[:,0:n-1]
    y=orginX[:,n-1]
    
    opt=Opt()
    parameter=Parameter(algorithm='poss')
    dimension=Dimension(n-1)#n represent the number of features
    Mse=MSE(X,y)
    objective=Objective(func=Mse.Loss, dim=dimension, constraint=8)
    print 'start'
    result=opt.min(objective, parameter)
    print result
