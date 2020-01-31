from zoopt import Objective, Dimension, Solution, Parameter, ExpOpt
import time


def sphere(solution):
    """
    Sphere function for continuous optimization
    """
    x = solution.get_x()
    value = sum([(i-0.2)*(i-0.2) for i in x])
    # time.sleep(2)
    return value


if __name__ == '__main__':
    dim = 100  # dimension
    objective = Objective(sphere, Dimension(dim, [[-1, 1]] * dim, [True] * dim))  # setup objective
    parameter = Parameter(budget=4000, seed=666, intermediate_freq=100, parallel=True, server_num=10)  # init with init_samples
    t1 = time.time()
    solution_list = ExpOpt.min(objective, parameter, repeat=1, plot=False)
    # t2 = time.time()
    # m, s = divmod(t2-t1, 60)
    # h, m = divmod(m, 60)
    # print('running time: %02d:%02d:%02d' % (h, m, s))
    for solution in solution_list:
        x = solution.get_x()
        value = solution.get_value()
        print(x, value)
    parameter = Parameter(budget=2000, seed=666, intermediate_freq=100)
    solution_list = ExpOpt.min(objective, parameter, repeat=1, plot=False)
    for solution in solution_list:
        x = solution.get_x()
        value = solution.get_value()
        print(x, value)