import sys
sys.path.append("/Users/liu/Desktop/CS/github/ZOO/")

from example.direct_policy_search_for_gym.gym_task import GymTask
from zoopt.opt_algorithms.asynchronous_racos import evaluation_server
from sys import argv
from random import Random


# test function
def run_server(ip, port, task_name, layers, max_step, repeat):
    for i in range(repeat):
        data_length = 2048
        server_ip = ip
        server_port = port

        gym_task = GymTask(task_name)  # choose a task by name
        gym_task.new_nnmodel(layers)  # construct a neural network
        gym_task.set_max_step(max_step)  # set max step in gym


        # set server ip, port and longest data length in initialization
        server = evaluation_server.CalculatorServer(server_ip, server_port, data_length)

        server.start_server(func=gym_task.sum_reward)

if __name__ == "__main__":
    ip = argv[1]
    port = int(argv[2])

    mountain_car_layers = [2, 5, 1]
    acrobot_layers = [6, 5, 3, 1]
    halfcheetah_layers = [17, 10, 6]
    humanoid_layers = [376, 25, 17]
    swimmer_layers = [8, 5, 3, 2]
    ant_layers = [111, 15, 8]
    hopper_layers = [11, 9, 5, 3]
    lunarlander_layers = [8, 5, 3, 1]

    run_test('MountainCar-v0', mountain_car_layers, 10000, 10000, 10)
    # run_test('Acrobot-v1', acrobot_layers, 2000, 500, 10)
    # If you want to run the following examples, you may need to install more libs(mujoco, Box2D).
    # run_test('HalfCheetah-v1', halfcheetah_layers, 2000, 10000, 10)
    # run_test('Humanoid-v1', humanoid_layers, 2000, 50000, 10)
    # run_test('Swimmer-v1', swimmer_layers, 2000, 10000, 10)
    # run_test('Ant-v1', ant_layers, 2000, 10000, 10)
    # run_test('Hopper-v1', hopper_layers, 2000, 10000, 10)
    # run_test('LunarLander-v2', lunarlander_layers, 2000, 10000, 10)
    run_server(ip, port, )


