import numpy as np
from zoo.opt import Opt
from zoo.parameter import Parameter
from zoo.objective import Objective
from zoo.dimension import Dimension
from math import exp
import codecs
import arff


class MSE:
    def __init__(self,X,y,k):
        self._best_solution = None
        self._X=X
        self._y=y
        self._C=X.T*X
        self._b=X.T*y
        self._size=np.shape(X)
        self._k=k
    def position(self,s):
        n=np.shape(s)[1]
        result=[]
        for i in range(0,n):
            if s[0,i]==1:
                result.append(i)
        return result  
      
    def constraint(self,solution):
        return self._k-solution[0,:].sum()#result is bigger than zero mean satisitying,otherwise
    
    def isolationfunction(self,solution):
            return 0#In this case isolationfunction is a constant
        
    def get_k(self):
        return self._k
     
    def loss(self,solution):
        if solution[0, :].sum()==0.0 or solution[0, :].sum()>=2.0*self._k:
            return float('inf')
        pos = self.position(solution)
        alpha = (self._C[pos, :])[:, pos].I*self._b[pos, :]
        sub = self._y - self._X[:, pos]*alpha
        mse=sub.T*sub/self._size[0]
        return mse


# Read data from file
def read_data(filename):
    file_ = codecs.open(filename, 'rb', 'utf-8')
    decoder = arff.ArffDecoder()
    dataset = decoder.decode(file_.readlines(), encode_nominal=True)
    file_.close()
    data = dataset['data']
    return np.mat(data)
#normalize data to have mean 0 and variance 1 for each column
def normlize_date(dataMatrix):
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
    data=read_data('sonar.arff')
    orginX=normlize_date(data)
    
    n=np.shape(orginX)[1]
    X=orginX[:,0:n-1]
    y=orginX[:,n-1]
    k=8
    opt=Opt()
    Mse=MSE(X,y,k)
    dimension=Dimension((n-1,k))#n represent the number of features
    parameter=Parameter(algorithm='poss')
    parameter.set_paretoopt_iteration_parameter(2*exp(1))
    parameter.set_isolationFunc(Mse.isolationfunction)
    objective=Objective(func=Mse.loss, dim=dimension, constraint=Mse.constraint)
    print 'start'
    result=opt.min(objective, parameter)
    print result
