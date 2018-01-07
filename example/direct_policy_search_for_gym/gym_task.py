"""
The class GymTask sets a gym runtime environment.

Author:
    Yu-Ren Liu
"""

import gym
from gym.spaces.discrete import Discrete
from nn_model import NNModel


class GymTask:
    """
    This class sets a gym runtime environment.
    """

    def __init__(self, name):
        """
        Init function.

        :param name: gym task name
        """
        self.reset_task()
        self.__envir = gym.make(name)  # gym environment
        self.__envir_name = name  # environment name
        self.__obser_size = self.__envir.observation_space.shape[0]  # the number of parameters in observation
        self.__obser_up_bound = []  # the upper bound of parameters in observation
        self.__obser_low_bound = []  # the lower bound of parameters in observation
        self.total_step = 0  # total s
        self.__action_size = None  # the number of parameters in action
        self.__action_sca = []  # environment action space, specified by gym
        self.__action_type = []  # the type of action, false means discrete
        self.__action_low_bound = []  # action lower bound
        self.__action_up_bound = []  # action upper bound
        # policy model, it's a neural network in this example
        self.__policy_model = None
        self.__max_step = 0  # maximum stop step
        self.__stop_step = 0  # the stop step in recent trajectory

        for i in range(self.__obser_size):
            self.__obser_low_bound.append(
                self.__envir.observation_space.high[i])
            self.__obser_up_bound.append(self.__envir.observation_space.low[i])

        # if the dimension of action space is one
        if isinstance(self.__envir.action_space, Discrete):
            self.__action_size = 1
            self.__action_sca = []
            self.__action_type = []
            self.__action_sca.append(self.__envir.action_space.n)
            self.__action_type.append(False)
        # if action object is Box
        else:
            self.__action_size = self.__envir.action_space.shape[0]
            self.__action_type = []
            self.__action_low_bound = []
            self.__action_up_bound = []
            for i in range(self.__action_size):
                self.__action_type.append(True)
                self.__action_low_bound.append(
                    self.__envir.action_space.low[i])
                self.__action_up_bound.append(
                    self.__envir.action_space.high[i])

    def reset_task(self):
        """
        Reset gym runtime environment.

        :return: no return value
        """
        self.__envir = None
        self.__envir_name = None
        self.__obser_size = None
        self.__obser_low_bound = []
        self.__obser_up_bound = []
        self.__action_type = []
        self.__policy_model = None
        self.__max_step = 0

    #
    def transform_action(self, temp_act):
        """
        Transform action from neural network into true action.

        :param temp_act: output of the neural network
        :return: action
        """
        action = []
        for i in range(self.__action_size):
            # if action is continue
            if self.__action_type[i]:
                tmp_act = (temp_act[i]+1)*((self.__action_up_bound[i] -
                                            self.__action_low_bound[i])/2.0)+self.__action_low_bound[i]
                action.append(tmp_act)
            else:
                sca = 2.0 / self.__action_sca[0]
                start = -1.0
                now_value = start + sca
                true_act = 0
                while now_value <= 1.0:
                    if temp_act[i] <= now_value:
                        break
                    else:
                        now_value += sca
                        true_act += 1
                if true_act >= self.__action_sca[i]:
                    true_act = self.__action_sca[i] - 1
                action.append(true_act)
        if self.__action_size == 1:
            action = action[0]
        return action

    def new_nnmodel(self, layers):
        """
        Generate a new model

        :param layers: layer information
        :return: no return
        """
        # initialize NN model as policy
        self.__policy_model = NNModel()
        self.__policy_model.construct_nnmodel(layers)

        return

    def nn_policy_sample(self, observation):
        """
        Generate action from observation using neuron network policy

        :param observation: observation is the output of gym task environment
        :return: action to choose
        """
        output = self.__policy_model.cal_output(observation)
        action = self.transform_action(output)
        return action

    def sum_reward(self, solution):
        """
        Objective function of racos by summation of reward in a trajectory

        :param solution: a data structure containing x and fx
        :return: value of fx
        """
        x = solution.get_x()
        sum_re = 0
        # reset stop step
        self.__stop_step = self.__max_step
        # reset nn model weight
        self.__policy_model.decode_w(x)
        # reset environment
        observation = self.__envir.reset()
        for i in range(self.__max_step):
            action = self.nn_policy_sample(observation)
            observation, reward, done, info = self.__envir.step(action)
            sum_re += reward
            if done:
                self.__stop_step = i
                break
            self.total_step += 1
        value = sum_re
        name = self.__envir_name
        # turn the direction for minimization
        if name == 'CartPole-v0' or name == 'CartPole-v1' or name == 'MountainCar-v0' or name == 'Acrobot-v1' or name == 'HalfCheetah-v1' \
                or name == 'Humanoid-v1' or name == 'Swimmer-v1' or name == 'Ant-v1' or name == 'Hopper-v1' \
                or name == 'LunarLander-v2' or name == 'BipedalWalker-v2':
            value = -value
        return value

    def get_environment(self):
        return self.__envir

    def get_environment_name(self):
        return self.__envir_name

    def get_observation_size(self):
        return self.__obser_size

    def get_observation_low_bound(self, index):
        return self.__obser_low_bound[index]

    def get_observation_upbound(self, index):
        return self.__obser_up_bound[index]

    def get_action_size(self):
        return self.__action_size

    def get_action_type(self, index):
        return self.__action_type[index]

    def get_stop_step(self):
        return self.__stop_step

    def get_w_size(self):
        return self.__policy_model.get_w_size()

    def set_max_step(self, ms):
        self.__max_step = ms
        return
