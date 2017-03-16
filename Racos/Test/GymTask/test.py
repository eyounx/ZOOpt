import gym
from gym import envs
env = gym.make('MountainCar-v0')
print(env.action_space.n)
#> Discrete(2)
print(env.observation_space)
print(env.observation_space.low)
print(env.observation_space.high)
print(envs.registry.all())
#> Box(4,)