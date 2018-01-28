# Optimization Example on Direct Policy Search for Reinforcement Learning

Direct policy search method is a kind of reinforcement learning approach that direct optimizes the parameters of the policy to maximize the total reward. This example is derived from the following paper 
> Yi-Qi Hu, Hong Qian, and Yang Yu. Sequential classification-based optimization for direct policy search. In: Proceedings of the 31st AAAI Conference on Artificial Intelligence (AAAI’17), San Francisco, CA, 2017.

A neural network model implemented in `nn_model.py` is used as the policy. In `gym_task.py`, reinforcement learning tasks in Gym are wrapped in the class as a derivative-free optimization problem. `run.py` provides examples of doing the policy search.

__Package requirement:__
* gym: https://gym.openai.com/docs
* numpy: http://www.numpy.org
