# Optimization Examples on Sparse Regression

`poss_opt.py` demonstrates the example of sparse regression using Pareto optimization. The example is derived from the following paper
> Chao Qian, Yang Yu and Zhi-Hua Zhou. Subset selection by Pareto optimization. In: Advances in Neural Information Processing Systems 28 (NIPS'15) , Montreal, Canada, 2015.

`ponss_opt.py` demonstrates the example of sparse regression using Pareto optimization with noise-aware strategy. The example is derived from the following paper
> Chao Qian, Jing-Cheng Shi, Yang Yu, Ke Tang, and Zhi-Hua Zhou. Subset selection under noise. In: Advances in Neural Information Processing Systems 30 (NIPS'17), Long Beach, CA, 2017.

For sparse regression, the objective is to learn a linear classifier _w_ minimzing the mean squared error, while the number of non-zero elements of _w_ should be not larger than _k_, which is a sparsity requirement.

The objective function can be write as    
```
min_w mse(w)   s.t.  ||w||_0 <= k
```

These examples show how to solve this problem using a subset selection algorithm called Pareto optimization, which has a better theoretical guarantee than greedy algorithm. Details can be find in the above papers.
 
 __Package requirement:__
* liac-arff: https://pypi.python.org/pypi/liac-arff
* numpy: http://www.numpy.org