# Optimization Example on Linear Classifier using Ramp-loss

Ramp-loss is a robust loss function for classification learning task. It is however non-convex. This example is derived from the following paper to minimize the ramp-loss.
> Yang Yu, Hong Qian, and Yi-Qi Hu. Derivative-free optimization via classification. In: Proceedings of the 30th AAAI Conference on Artificial Intelligence (AAAI'16), Phoenix, AZ, 2016, pp.2286-2292.

In `ramploss.py`, a class RampLoss is defined to handle the loss function calculation and file reading. You can run this file to get results of this example. `ionosphere.arff` is an example data set.

__Package requirement:__
* liac-arff: https://pypi.python.org/pypi/liac-arff

