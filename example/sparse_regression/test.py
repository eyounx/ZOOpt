from zoo.algos.paretoopt.ParetoOptimization import ParetoOptimization
#from zoo.algos.racos.racos_optimization import RacosOptimization
import numpy as np
from zoo.algos.paretoopt.NormalizeData import NormlizeDate

from zoo.opt import Opt
from zoo.parameter import Parameter
from zoo.objective import Objective

if __name__=='__main__':
    opt=Opt()
    parameter=Parameter()
    objective=Objective()
    orginX=NormlizeDate("housing.txt")
    n=np.shape(orginX)[1]
    X=orginX[:,0:n-1]
    y=orginX[:,n-1]
    parameter.set_paretoopt_parameters(X,y,8)
    parameter.set_algorithm('poss')
    objective.set_constraint(True)
    result=opt.min(objective, parameter)
    print result