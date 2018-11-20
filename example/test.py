import numpy as np
from zoopt import Dimension, Objective, Parameter, ExpOpt, Solution, Opt
from zoopt.utils.zoo_global import gl

def fn(solution):
    x = solution.get_x()
    x1 = [0,3,1,0,0]
    # print(x)
    val = sum([abs(v-x1[i]) for i,v in enumerate(x)])+ ((np.sum([i for i in x[0:3]])-1.0)**2)
    return val

dim = 5
gl.set_seed(0)
dimobj = Dimension(dim, regs=[[0,5]]*dim, tys=[False]*dim)
obj = Objective(fn, dimobj)
param = Parameter(budget=1000)
solution = Opt.min(obj, param)
print(solution.get_x(), solution.get_value())