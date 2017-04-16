This RACOS algorithm was implemented in python

Directory Layout:
zoo:
    algos
        racos
	       racos.py
           racos_classification.py
           racos_common.py
           racos_optimization.py
           sracos.py
	   poss
	       paretoopt.py
    utils
        my_global.py
        tool_function.py
    dimension.py
    objective.py
    opt.py
    parameter.py
    solution.py
docs
example

How to use this package?
Examples are listed in the directory 'examples'，you can follow these steps to optimize.
1.Import related packages
2.You should construct a dim
3.Define your objective function. You can refer to objective functions defined in fx.py(example/simple_functions/fx.py)
3.Use dim and objective function to construct an objective
4.Construct parameter, which includes at least the algorithm you want to use and budget
5.Optimize

eg.:
from example.simple_functions.fx import ackley
from zoo.dimension import Dimension
from zoo.objective import Objective
from zoo.parameter import Parameter
from zoo.opt import Opt
        
dim_size = 10
dim_regs = [[-1, 1]] * dim_size
dim_tys = [True] * dim_size
dim = Dimension(dim_size, dim_regs, dim_tys)
objective = Objective(ackley, dim)
budget = 50000
parameter = Parameter(algorithm="racos", budget=budget)
solution = Opt.min(objective, parameter)
solution.print_solution()
