
from gym_task import GymTask
from zoopt import Dimension, Objective, Parameter, Opt, Solution

"""
Function run_test is defined in this file. You can run this file to get results of this example.

Author:
    Yuren Liu
"""


# test function


# in_layers means layers information. eg. [2, 5, 1] means input layer has 2 neurons, hidden layer(only one) has 5,
# output layer has 1.
# in_budget means budget
# maxstep means stop step in gym
# repeat means repeat number in a test.
def run_test(task_name, layers, in_budget, max_step, repeat):

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

    objective = Objective(gym_task.sum_reward, dim)  # form up the objective function
    parameter = Parameter(budget=budget, autoset=True)  # by default, the algorithm is sequential RACOS
    parameter.set_probability(rand_probability)

    result = []
    sum = 0
    print('solved solution is:')
    for i in range(repeat):
        ins = Opt.min(objective, parameter)
        result.append(ins.get_value())
        sum += ins.get_value()
        ins.print_solution()
    print(result)  # results in repeat times
    print(sum/len(result))  # average result

if __name__ == '__main__':
        mountain_car_layers = [2, 5, 1]
        acrobot_layers = [6, 5, 3, 1]
        halfcheetah_layers = [17, 10, 6]
        humanoid_layers = [376, 25, 17]
        swimmer_layers = [8, 5, 3, 2]
        ant_layers = [111, 15, 8]
        hopper_layers = [11, 9, 5, 3]
        lunarlander_layers = [8, 5, 3, 1]
        run_test('MountainCar-v0', mountain_car_layers, 2000, 10000, 1)
        # run_test('Acrobot-v1', acrobot_layers, 2000, 2000, 1)
        # If you want to run the following examples, you may need to install more libs(mujoco, Box2D).
        # run_test('HalfCheetah-v1', halfcheetah_layers, 2000, 10000, 10)
        # run_test('Humanoid-v1', humanoid_layers, 2000, 50000, 10)
        # run_test('Swimmer-v1', swimmer_layers, 2000, 10000, 10)
        # run_test('Ant-v1', ant_layers, 2000, 10000, 10)
        # run_test('Hopper-v1', hopper_layers, 2000, 10000, 10)
        # run_test('LunarLander-v2', lunarlander_layers, 2000, 10000, 10)