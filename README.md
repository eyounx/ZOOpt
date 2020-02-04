# ZOOpt

[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/eyounx/ZOOpt/blob/master/LICENSE.txt) [![Build Status](https://www.travis-ci.org/eyounx/ZOOpt.svg?branch=master)](https://www.travis-ci.org/eyounx/ZOOpt) [![Documentation Status](https://readthedocs.org/projects/zoopt/badge/?version=latest)](https://zoopt.readthedocs.io/en/latest/?badge=latest) [![codecov](https://codecov.io/gh/AlexLiuyuren/ZOOpt/branch/master/graph/badge.svg)](https://codecov.io/gh/AlexLiuyuren/ZOOpt)

ZOOpt is a python package for Zeroth-Order Optimization. 

Zeroth-order optimization (a.k.a. derivative-free optimization/black-box optimization) does not rely on the gradient of the objective function, but instead, learns from samples of the search space. It is suitable for optimizing functions that are nondifferentiable, with many local minima, or even unknown but only testable.

ZOOpt implements some state-of-the-art zeroth-order optimization methods and their parallel versions. Users only need to add several keywords to use parallel optimization on a single machine. For large-scale distributed optimization across multiple machines, please refer to [Distributed ZOOpt](https://github.com/eyounx/ZOOsrv).  

**Documents**: [Tutorial of ZOOpt](http://zoopt.readthedocs.io/en/latest/index.html)

**Citation**: 

> **Yu-Ren Liu, Yi-Qi Hu, Hong Qian, Yang Yu, Chao Qian. ZOOpt: Toolbox for Derivative-Free Optimization**. [CORR abs/1801.00329](https://arxiv.org/abs/1801.00329)

(Features in this article are from version 0.2)

## Installation 

The easiest way to install ZOOpt is to type `pip install zoopt` in the terminal/command line.

Alternatively, to install ZOOpt by source code, download this repository and sequentially run following commands in your terminal/command line.

```
$ python setup.py build
$ python setup.py install
```

## A simple example

We define the Ackley function for minimization (note that this function is for arbitrary dimensions, determined by the solution)

```python
import numpy as np
def ackley(solution):
    x = solution.get_x()
    bias = 0.2
    value = -20 * np.exp(-0.2 * np.sqrt(sum([(i - bias) * (i - bias) for i in x]) / len(x))) - \
            np.exp(sum([np.cos(2.0*np.pi*(i-bias)) for i in x]) / len(x)) + 20.0 + np.e
    return value
```

Ackley function is a classical function with many local minima. In 2-dimension, it looks like (from wikipedia)

<table border=0><tr><td width="400px"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Ackley%27s_function.pdf/page1-400px-Ackley%27s_function.pdf.jpg" alt="Ackley function"/></td></tr></table>
 Then, use ZOOpt to optimize a 100-dimension Ackley function:

```python
from zoopt import Dimension, Objective, Parameter, Opt, ExpOpt

dim = 100  # dimension
obj = Objective(ackley, Dimension(dim, [[-1, 1]]*dim, [True]*dim))
# perform optimization
solution = Opt.min(obj, Parameter(budget=100*dim))
# print the solution
print(solution.get_x(), solution.get_value())
# parallel optimization for time-consuming tasks
solution = Opt.min(obj, Parameter(budget=100*dim, parallel=True, server_num=3))
```

For a few seconds, the optimization is done. Then, we can visualize the optimization progress

```python
import matplotlib.pyplot as plt
plt.plot(obj.get_history_bestsofar())
plt.savefig('figure.png')
```

which looks like

<table border=0><tr><td width="400px"><img src="https://github.com/eyounx/ZOOpt/blob/dev/img/quick_start.png?raw=true" alt="Expeirment results"/></td></tr></table>
We can also use `ExpOpt` to repeat the optimization for performance analysis, which will calculate the mean and standard deviation of multiple optimization results while automatically visualizing the optimization progress.

```python
solution_list = ExpOpt.min(obj, Parameter(budget=100*dim), repeat=3,
                           plot=True, plot_file="progress.png")
for solution in solution_list:
		print(solution.get_x(), solution.get_value())

```

More examples are available in the `example` fold.

# Releases

## [release 0.3](https://github.com/eyounx/ZOOpt/releases/tag/v0.3)

- Add a parallel implementation of SRACOS, which accelarates the optimization by asynchronous parallelization.
- Add a function that enables users to set  a customized stop criteria for the optimization.
- Rewrite the documentation to make it easier to follow.

## [release 0.2](https://github.com/eyounx/ZOOpt/releases/tag/v0.2.1)

- Add the noise handling strategies Re-sampling and Value Suppression (AAAI'18), and the subset selection method with noise handling PONSS (NIPS'17)
- Add high-dimensionality handling method Sequential Random Embedding (IJCAI'16) 
- Rewrite Pareto optimization method. Bugs fixed.

## [release 0.1](https://github.com/eyounx/ZOOpt/releases/tag/v0.1)

- Include the general optimization method RACOS (AAAI'16) and Sequential RACOS (AAAI'17), and the subset selection method POSS (NIPS'15).
- The algorithm selection is automatic. See examples in the `example` fold.- Default parameters work well on many problems, while parameters are fully controllable
- Running speed optmized for Python

# Distributed ZOOpt

Distributed ZOOpt is consisted of a [server project](https://github.com/eyounx/ZOOsrv) and a [client project](https://github.com/eyounx/ZOOclient.jl). Details can be found in the [Tutorial of Distributed ZOOpt](http://zoopt.readthedocs.io/en/latest/Tutorial%20of%20Distributed%20ZOOpt.html)

