import gym
from gym.spaces.discrete import Discrete
from NNModel_theano import NNModel
import theano
import theano.tensor as T


class GymTask:
    __envir = None                      # environment object
    __envir_name = None                 # environment name
    __obser_size = None                 # the number of parameters in observation
    __obser_low_bound = []              # the lower bound of parameters in observation
    __obser_up_bound = []               # the upper bound of parameters in observation
    __action_size = None                # the number of parameters in action
    __action_sca = []
    __action_type = []                  # the type of action, false means discrete
    __action_low_bound = []
    __action_up_bound = []
    __policy_model = None
    __max_step = 0
    __stop_step = 0                     # the stop step in recent trajectory

    def __init__(self, name):
        self.reset_task()
        self.__envir = gym.make(name)
        self.__envir_name = name
        self.__obser_size = self.__envir.observation_space.shape[0]
        self.__obser_up_bound = []
        self.__obser_low_bound = []
        for i in range(self.__obser_size):
            self.__obser_low_bound.append(self.__envir.observation_space.high[i])
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
                self.__action_low_bound.append(self.__envir.action_space.low[i])
                self.__action_up_bound.append(self.__envir.action_space.high[i])
        # for i in range(self.__action_size):
        #     self.__action_type.append(False)

    def reset_task(self):
        self.__envir = None
        self.__envir_name = None
        self.__obser_size = None
        self.__obser_low_bound = []
        self.__obser_up_bound = []
        self.__action_type = []
        self.__policy_model = None
        self.__max_step = 0

    # Transform action from neural network into true action.
    def transform_action(self, temp_act):
        # print temp_act
        action = []
        for i in range(self.__action_size):
            # if action is continue
            if self.__action_type[i]:
                tmp_act = (temp_act[i]+1)*((self.__action_up_bound[i]-self.__action_low_bound[i])/2.0)+self.__action_low_bound[i]
                action.append(tmp_act)
            else:
                sca = 2.0 / self.__action_sca[0]
                start = -1.0
                now_value = start + sca
                true_act = 0
                while now_value <= 1.0:
                    if theano.tensor.ge(now_value, temp_act[i]):
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

    # generate a new model
    def new_nnmodel(self, layers):
        # initialize NN model as policy
        self.__policy_model = NNModel()
        self.__policy_model.construct_nnmodel(layers)

        return

    # generate action from observation using neuron network policy
    def nn_policy_sample(self, observation):
        # action = []
        output = self.__policy_model.cal_output(observation)
        # print 'output:', output
        action = self.transform_action(output)
        return action

    # objective function of racos by summation of reward in a trajectory
    def sum_reward(self, x):
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
        value = sum_re
        name = self.__envir_name
        if name == 'CartPole-v0' or name == 'MountainCar-v0' or name == 'Acrobot-v1' or name == 'HalfCheetah-v1' \
                or name == 'Humanoid-v1' or name == 'Swimmer-v1' or name == 'Ant-v1' or name == 'Hopper-v1' \
                or name == 'LunarLander-v2' or name == 'BipedalWalker-v2':
            value = -value
        # print value
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