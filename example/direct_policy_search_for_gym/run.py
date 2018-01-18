"""
Function run_test is defined in this file. You can run this file to get results of this example.

Author:
    Yu-Ren Liu
"""
from gym_task import GymTask
from zoopt import Dimension, Objective, Parameter, ExpOpt, Opt


def run_test(task_name, layers, in_budget, max_step, repeat, terminal_value=None):
    """
    example of running direct policy search for gym task.

    :param task_name: gym task name
    :param layers:
        layer information of the neural network
        e.g., [2, 5, 1] means input layer has 2 neurons, hidden layer(only one) has 5 and output layer has 1
    :param in_budget:  number of calls to the objective function
    :param max_step: max step in gym
    :param repeat:  repeat number in a test
    :param terminal_value: early stop, algorithm should stop when such value is reached
    :return: no return value
    """
    gym_task = GymTask(task_name)  # choose a task by name
    gym_task.new_nnmodel(layers)  # construct a neural network
    gym_task.set_max_step(max_step)  # set max step in gym

    budget = in_budget  # number of calls to the objective function
    rand_probability = 0.95  # the probability of sample in model

    # set dimension
    dim_size = gym_task.get_w_size()
    dim_regs = [[-10, 10]] * dim_size
    dim_tys = [True] * dim_size
    dim = Dimension(dim_size, dim_regs, dim_tys)

    # form up the objective function
    objective = Objective(gym_task.sum_reward, dim)
    parameter = Parameter(budget=budget, terminal_value=terminal_value)
    parameter.set_probability(rand_probability)

    solution_list = ExpOpt.min(objective, parameter, repeat=repeat)


def run_test_handlingnoise(task_name, layers, in_budget, max_step, repeat, terminal_value):
    """
    example of running direct policy search for gym task with noise handling.

    :param task_name: gym task name
    :param layers:
        layer information of the neural network
        e.g., [2, 5, 1] means input layer has 2 neurons, hidden layer(only one) has 5 and output layer has 1
    :param in_budget:  number of calls to the objective function
    :param max_step: max step in gym
    :param repeat:  number of repeatitions for noise handling
    :param terminal_value: early stop, algorithm should stop when such value is reached
    :return: no return value
    """
    gym_task = GymTask(task_name)  # choose a task by name
    gym_task.new_nnmodel(layers)  # construct a neural network
    gym_task.set_max_step(max_step)  # set max step in gym

    budget = in_budget  # number of calls to the objective function
    rand_probability = 0.95  # the probability of sample in model

    # set dimension
    dim_size = gym_task.get_w_size()
    dim_regs = [[-10, 10]] * dim_size
    dim_tys = [True] * dim_size
    dim = Dimension(dim_size, dim_regs, dim_tys)
    # form up the objective function
    objective = Objective(gym_task.sum_reward, dim)
    # by default, the algorithm is sequential RACOS
    parameter = Parameter(budget=budget, autoset=True,
                          suppression=True, terminal_value=terminal_value)
    parameter.set_resample_times(70)
    parameter.set_probability(rand_probability)

    solution_list = ExpOpt.min(objective, parameter, repeat=repeat)


if __name__ == '__main__':
    CartPole_layers = [4, 5, 1]
    mountain_car_layers = [2, 5, 1]
    acrobot_layers = [6, 5, 3, 1]
    halfcheetah_layers = [17, 10, 6]
    humanoid_layers = [376, 25, 17]
    swimmer_layers = [8, 5, 3, 2]
    ant_layers = [111, 15, 8]
    hopper_layers = [11, 9, 5, 3]
    lunarlander_layers = [8, 5, 3, 1]

    run_test('MountainCar-v0', mountain_car_layers, 2000, 1000, 1)
    run_test_handlingnoise('MountainCar-v0', mountain_car_layers,  1000, 1000, 5, terminal_value=-500)
    # run_test('Acrobot-v1', acrobot_layers, 2000, 500, 10)
    # If you want to run the following examples, you may need to install more libs(mujoco, Box2D).
    # run_test('HalfCheetah-v1', halfcheetah_layers, 2000, 10000, 10)
    # run_test('Humanoid-v1', humanoid_layers, 2000, 50000, 10)
    # run_test('Swimmer-v1', swimmer_layers, 2000, 10000, 10)
    # run_test('Ant-v1', ant_layers, 2000, 10000, 10)
    # run_test('Hopper-v1', hopper_layers, 2000, 10000, 10)
    # run_test('LunarLander-v2', lunarlander_layers, 2000, 10000, 10)
