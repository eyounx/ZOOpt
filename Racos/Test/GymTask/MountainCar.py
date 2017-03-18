from NNModel import NNModel, Layer
from GymTask import GymTask
from Racos.Component.Dimension import Dimension
from Racos.Component.Objective import Objective
from Racos.Component.Parameter import Parameter
from Racos.Method.RacosOptimization import RacosOptimization
# import FileOperator as fo

# test function


def run_test():
    layers = [2, 5, 1]

    task_name = 'MountainCar-v0'

    max_step = 10000

    gym_task = GymTask(task_name)
    gym_task.new_nnmodel(layers)
    gym_task.set_max_step(max_step)

    sample_size = 20  # the instance number of sampling in an iteration
    max_iteration = 100  # the number of iterations
    budget = 2000  # budget in online style 2000
    positive_num = 2  # the set size of PosPop
    rand_probability = 0.95  # the probability of sample in model
    uncertain_bits = 1  # the dimension size that is sampled randomly

    # set dimension
    dim_size = gym_task.get_w_size()
    dim_regs = []
    dim_tys = []
    for i in range(dim_size):
        dim_regs.append([-10, 10])
        dim_tys.append(True)
    dim = Dimension(dim_size, dim_regs, dim_tys)
    objective = Objective(gym_task.sum_reward, dim)
    parameter = Parameter(objective, budget)
    parameter.set_probability(rand_probability)
    racos = RacosOptimization()
    print 'Best solution is:'
    ins = racos.opt(parameter, strategy='WR', ub=uncertain_bits)
    ins.print_instance()

run_test()
