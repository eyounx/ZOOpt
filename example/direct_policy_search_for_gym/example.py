from gym_task import GymTask
from zoo.dimension import Dimension
from zoo.objective import Objective
from zoo.parameter import Parameter
from zoo.opt import Opt

# test function


def run_test(name, in_layers, in_budget, maxstep, repeat):
    layers = in_layers

    task_name = name

    max_step = maxstep

    gym_task = GymTask(task_name)
    gym_task.new_nnmodel(layers)
    gym_task.set_max_step(max_step)

    budget = in_budget  # budget in online style 2000
    rand_probability = 0.95  # the probability of sample in model

    # set dimension
    dim_size = gym_task.get_w_size()
    dim_regs = [[-10, 10]] * dim_size
    dim_tys = [True] * dim_size
    dim = Dimension(dim_size, dim_regs, dim_tys)
    objective = Objective(gym_task.sum_reward, dim)
    parameter = Parameter(budget=budget, autoset=True)
    parameter.set_probability(rand_probability)
    print 'Best solution is:'
    result = []
    sum = 0
    for i in range(repeat):
        ins = Opt.min(objective, parameter)
        result.append(ins.get_value())
        sum += ins.get_value()
        ins.print_solution()
    print result
    print sum/len(result)

if __name__ == '__main__':
    mountain_car_layers = [2, 5, 1]
    acrobot_layers = [6, 5, 3, 1]
    halfcheetah_layers = [17, 10, 6]
    humanoid_layers = [376, 25, 17]
    swimmer_layers = [8, 5, 3, 2]
    ant_layers = [111, 15, 8]
    hopper_layers = [11, 9, 5, 3]
    lunarlander_layers = [8, 5, 3, 1]
    run_test('MountainCar-v0', mountain_car_layers, 2000, 10000, 5)
    run_test('Acrobot-v1', acrobot_layers, 2000, 2000, 5)
    # If you want to run the following examples, you may need to install more libs(mujoco, Box2D).
    # run_test('HalfCheetah-v1', halfcheetah_layers, 2000, 10000, 10)
    # run_test('Humanoid-v1', humanoid_layers, 2000, 50000, 10)
    # run_test('Swimmer-v1', swimmer_layers, 2000, 10000, 10)
    # run_test('Ant-v1', ant_layers, 2000, 10000, 10)
    # run_test('Hopper-v1', hopper_layers, 2000, 10000, 10)
    # run_test('LunarLander-v2', lunarlander_layers, 2000, 10000, 10)