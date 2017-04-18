# Optimization Example on Sparse Regression

`example.py` demonstrates the example of sparse regression using Pareto optimization. The example is derived from the following paper
> Chao Qian, Yang Yu and Zhi-Hua Zhou. Subset selection by Pareto optimization. In: Advances in Neural Information Processing Systems 28 (NIPS'15) , Montreal, Canada, 2015.

For sparse regression, the objective is to learn a linear classifier _w_ minimzing the mean squared error, while the number of non-zero elements of _w_ should be not larger than _k_, which is a sparsity requirement.

The objective function can be write as    
```
min_w mse(w)   s.t.  ||w||_0 <= k
```

This example shows how to solve this problem using a subset selection algorithm called Pareto optimization, which has a better theoretical guarantee than greedy algorithm. Details can be find in the above paper.
 
 __Package requirement:__
* liac-arff: https://pypi.python.org/pypi/liac-arff
* numpy: http://www.numpy.org