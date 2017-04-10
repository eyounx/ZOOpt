from zoo.algos.racos.racos_optimization import RacosOptimization


class Opt:
    def __init__(self):
        return

    def min(self, objective, parameter):
        algorithm = parameter.get_algorithm()
        constraint = parameter.get_constraint()
        result = None
        if algorithm == 'poss' or ((constraint is not None) and (objective.get_dim().is_discrete() is True)):
            # TODO
            pass
        else:
            optimizer = RacosOptimization()
            result = optimizer.opt(objective, parameter)
        return result
