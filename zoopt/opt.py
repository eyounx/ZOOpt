"""
This module contains the class Opt.

Author:
    Yu-Ren Liu
"""
from zoopt.algos.paretoopt.ParetoOptimization import ParetoOptimization
from zoopt.algos.racos.racos_optimization import RacosOptimization
from zoopt.utils.zoo_global import gl
from zoopt.utils.tool_function import ToolFunction
from zoopt.random_embedding.sre_optimization import SequentialRandomEmbedding


class Opt:
    """
    Main entrance of optimization.
    """
    def __init__(self):
        return

    @staticmethod
    def min(objective, parameter):
        """
        Minimization function.

        :param objective: objective
        :param parameter: parameter
        :return: result of optimization
        """
        Opt.set_global(parameter)
        constraint = objective.get_constraint()
        algorithm = parameter.get_algorithm()
        if algorithm:
            algorithm = algorithm.lower()
        result = None
        if constraint is not None and ((algorithm is None) or (algorithm == "poss")):
            optimizer = ParetoOptimization()
        elif constraint is None and ((algorithm is None) or (algorithm == "racos") or (algorithm == "sracos")) or (algorithm == "ssracos"):
            optimizer = RacosOptimization()
        else:
            ToolFunction.log(
                "opt.py: No proper algorithm found for %s" % algorithm)
            return result
        if objective.get_sre() is True:
            sre = SequentialRandomEmbedding(objective, parameter, optimizer)
            result = sre.opt()
        else:
            result = optimizer.opt(objective, parameter)
        return result

    @staticmethod
    def set_global(parameter):
        """
        Set global variables.

        :param parameter: parameter
        :return: no return
        """

        precision = parameter.get_precision()
        if precision:
            gl.set_precision(precision)
