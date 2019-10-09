import numpy as np
from zoopt import Objective, Parameter, ExpOpt, Dimension, Opt
from simple_function import ackley, sphere


class StoppingCriterion:
    """
        This class defines a stopping criterion, which is used as a parameter of the class Parameter, and should implement
        check(self, optcontent) member function.
    """
    def __init__(self):
        self.__best_result = 0
        self.__count = 0
        self.__total_count = 0
        self.__count_limit = 100

    def check(self, optcontent):
        """
        This function is invoked at each iteration of the optimization.
        Optimization will stop early when this function returns True, otherwise, it is not affected. In this example,
        optimization will be stopped if the best result remains unchanged for 100 iterations.
        :param optcontent: an instance of the class RacosCommon. Several functions can be invoked to get the contexts of
        the optimization, which are listed as follows,
        optcontent.get_best_solution(): get the current optimal solution
        optcontent.get_data(): get all the solutions contained in the current solution pool
        optcontent.get_positive_data(): get positive solutions contained in the current solution pool
        optcontent.get_negative_data(): get negative solutions contained in the current solution pool

        :return: bool object.
        """
        self.__total_count += 1
        content_best_value = optcontent.get_best_solution().get_value()
        if content_best_value == self.__best_result:
            self.__count += 1
        else:
            self.__best_result = content_best_value
            self.__count = 0
        if self.__count >= self.__count_limit:
            print("stopping criterion holds, total_count: %d" % self.__total_count)
            return True
        else:
            return False


if __name__ == '__main__':
    dim_size = 100
    # form up the objective function
    objective = Objective(sphere, Dimension(dim_size, [[-1, 1]] * dim_size, [True] * dim_size))

    budget = 100 * dim_size
    # if intermediate_result is True, ZOOpt will output intermediate best solution every intermediate_freq budget
    parameter = Parameter(budget=budget, intermediate_result=True,
                          intermediate_freq=10, stopping_criterion=StoppingCriterion())
    sol = Opt.min(objective, parameter)
    sol.print_solution()