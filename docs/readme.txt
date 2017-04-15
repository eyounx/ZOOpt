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

The necessary files for RACOS are Components.py, Racos.py and Tools.py. The RACOS algorithm was implemented in Racos.py. There are some test functions in ObjectiveFunction.py, you can implement other tasks in other file. In Run_Racos.py, There are some demos of calling RACOS.
