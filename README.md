# ZOOpt
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/eyounx/ZOOpt/blob/master/LICENSE.txt)

A python package of Zeroth-Order Optimization (ZOOpt). 

Zeroth-order optimization (a.k.a. derivative-free optimization/black-box optimization) does not rely on the gradient of the objective function, but instead, learns from samples of the search space. It is suitable for optimizing functions that are nondifferentiable, with many local minima, or even unknown but only testable.

**Install**: `pip install zoopt`

## A quick example
We define the Ackley function for minimization using Theano
```python
import math, theano, theano.tensor as T
x = T.dvector('x')
f = theano.function([x], -20 * T.exp(-0.2 * T.sqrt((T.dot(x - 0.2, x - 0.2)).mean())) - T.exp(
    (T.cos(2 * math.pi * (x - 0.2))).mean()) + math.e + 20)
```
Ackley function is a classical function with many local minima. In 2-dimension, it looks like (from wikipedia)
<table border=0><tr><td width="400px"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Ackley%27s_function.pdf/page1-400px-Ackley%27s_function.pdf.jpg" alt="Expeirment results"/></td></tr></table>

Then, use ZOOpt to optimize a 100-dimension Ackley function
```python
from zoopt import Dimension, Objective, Parameter, Opt, Solution
dim = 100 # dimension
obj = Objective(lambda s: f(s.get_x()), Dimension(dim, [[-1, 1]] * dim, [True] * dim)) # setup objective
# perform optimization
solution = Opt.min(obj, Parameter(budget=100 * dim))
# print result
solution.print_solution()
```
For a few seconds, the optimization is done. Then, we can visualize the optimization progress
```python
from matplotlib import pyplot
pyplot.plot(obj.get_history_bestsofar())
pyplot.savefig('figure.png')
```
which looks like
<table border=0><tr><td width="400px"><img src="https://github.com/eyounx/TMP/blob/master/ZOO/figure.png?raw=true" alt="Expeirment results"/></td></tr></table>

More examples are available in the `example` fold.

## release 0.1
- Include the general optimization method RACOS (AAAI'16) and Sequential RACOS (AAAI'17), and the subset selection method POSS (NIPS'15).
- The algorithm selection is automatic. See examples in the `example` fold.
- Default parameters work well on many problems, while parameters are fully controllable
- Running speed optmized for Python
