
from zoo.algos.paretoopt.ParetoOptimization import ParetoOptimization
from zoo.algos.racos.racos_optimization import RacosOptimization
from zoo.utils.zoo_global import gl
from zoo.utils.tool_function import ToolFunction

"""
The class Opt is the main entrance of using zoo: Opt.min(objective, parameter)

Author:
    Yuren Liu
"""


class Opt:
    def __init__(self):
        return

    @staticmethod
    def min(objective, parameter):
        Opt.set_global(parameter)
        constraint = objective.get_constraint()
        algorithm = parameter.get_algorithm()
        if algorithm:
            algorithm = algorithm.lower()
        result = None
        if constraint is not None and ((algorithm is None) or (algorithm == "poss")):
            optimizer = ParetoOptimization()
            result = optimizer.opt(objective, parameter)
        elif constraint is None and ((algorithm is None) or (algorithm == "racos")):
            optimizer = RacosOptimization()
            result = optimizer.opt(objective, parameter)
        else:
            ToolFunction.log("opt.py: No proper algorithm find for %s" % algorithm)
        return result

    @staticmethod
    def set_global(parameter):
        precision = parameter.get_precision()
        if precision:
            gl.set_precision(precision)
