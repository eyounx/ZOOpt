from zoo.algos.racos.racos_optimization import RacosOptimization


class Optimizer:
    def __init__(self):
        return

    def min(self, objective, parameter):
        constraint = objective.get_constraint()
        algorithm = parameter.get_algorithm()
        if algorithm:
            algorithm = algorithm.lower()
        result = None
        if constraint is not None and ((algorithm is None) or (algorithm == "poss")):
            # TODO
            pass
        elif constraint is None and ((algorithm is None) or (algorithm == "racos")):
            optimizer = RacosOptimization()
            result = optimizer.opt(objective, parameter)
        else:
            print "No proper algorithm find for %s" % algorithm
        return result
