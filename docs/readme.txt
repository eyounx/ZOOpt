Directory Layout:
|--zoo:
    |--algos
        |--racos
               racos.py
               racos_classification.py
               racos_common.py
               racos_optimization.py
               sracos.py
	    |--paretoopt
	           paretoopt.py
    |--utils
        my_global.py
        tool_function.py
|--docs
|--example
dimension.py
objective.py
opt.py
parameter.py
solution.py

How to use this package?
Examples are listed in the directory 'example'.Briefly, you can follow these steps to optimize.
1.Import related packages
2.Construct a dim
3.Define your objective function. You can refer to objective functions defined in fx.py(example/simple_functions/fx.py)
4.Use dim and objective function to construct an objective
5.Construct parameter, which includes at least the algorithm you want to use and budget(If you want to use poss, budget
is not necessary)
6.Optimize

eg.:
from example.simple_functions.fx import ackley
from zoo.dimension import Dimension
from zoo.objective import Objective
from zoo.parameter import Parameter
from zoo.opt import Opt
from zoo.utils.my_global import gl

dim_size = 10
dim_regs = [[-1, 1]] * dim_size
dim_tys = [True] * dim_size
dim = Dimension(dim_size, dim_regs, dim_tys)
objective = Objective(ackley, dim)
budget = 50000
parameter = Parameter(algorithm="racos", budget=budget)
gl.set_seed(12345)
solution = Opt.min(objective, parameter)
solution.print_solution()

To know more about functions and parameters. Please refer to comments in corresponding files.