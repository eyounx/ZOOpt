---------------
Quick Start
---------------

ZOOpt is a python package for `Zeroth-Order Optimization <https://github.com/eyounx/ZOOpt/wiki/Derivative-Free-Optimization>`__. 

Zeroth-order optimization (a.k.a. derivative-free optimization/black-box optimization) does not rely on the gradient of the objective function, but instead, learns from samples of the search space. It is suitable for optimizing functions that are nondifferentiable, with many local minima, or even unknown but only testable.

ZOOpt implements some state-of-the-art zeroth-order optimization methods and their parallel versions. Users only need to add serveral keywords to use parallel optimization on a single machine. For large-scale distributed optimization across multiple machines, please refer to `Distributed ZOOpt <https://github.com/eyounx/ZOOsrv>`__.  

.. contents:: Table of Contents

Required packages
-----------------

This package requires the following packages:

-  Python version 2.7 or above 3.5
-  ``numpy`` http://www.numpy.org
-  ``matplotlib`` http://matplotlib.org/ (optional for plot drawing)

The easiest way to get these is to use
`pip <https://pypi.python.org/pypi/pip>`__ or
`conda <https://www.anaconda.com/what-is-anaconda/>`__ environment
manager. Typing the following command in your terminal will install all
required packages in your Python environment.

.. code:: console

    $ conda install numpy matplotlib

or

.. code:: console

    $ pip install numpy matplotlib

Getting and installing ZOOpt
----------------------------

The easiest way to install ZOOpt is to type ``pip install zoopt`` in you
terminal/command line.

If you want to install ZOOpt by source code, download this project and
sequentially run following commands in your terminal/command line.

.. code:: console

    $ python setup.py build
    $ python setup.py install

A quick example
---------------

We define the Ackley function for minimization (note that this function is for arbitrary dimensions, determined by the solution)

.. code:: python

    import numpy as np
    def ackley(solution):
        x = solution.get_x()
        bias = 0.2
        value = -20 * np.exp(-0.2 * np.sqrt(sum([(i - bias) * (i - bias) for i in x]) / len(x))) - \
                np.exp(sum([np.cos(2.0*np.pi*(i-bias)) for i in x]) / len(x)) + 20.0 + np.e
        return value

Ackley function is a classical function with many local minima. In 2-dimension, it looks like (from wikipedia)

.. image:: https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Ackley%27s_function.pdf/page1-400px-Ackley%27s_function.pdf.jpg
   :width: 400px
   :alt: Ackley function

Then, use ZOOpt to optimize a 100-dimension Ackley function:

.. code:: python

    from zoopt import Dimension, ValueType, Dimension2, Objective, Parameter, Opt, ExpOpt

    dim_size = 100  # dimension
    dim = Dimension(dim_size, [[-1, 1]]*dim_size, [True]*dim_size)  # or dim = Dimension2([(ValueType.CONTINUOUS, [-1, 1], 1e-6)]*dim_size)
    obj = Objective(ackley, dim)
    # perform optimization
    solution = Opt.min(obj, Parameter(budget=100*dim_size))
    # print the solution
    print(solution.get_x(), solution.get_value())
    # parallel optimization for time-consuming tasks
    solution = Opt.min(obj, Parameter(budget=100*dim_size, parallel=True, server_num=3))

Note that two classes are provided for constructing dimensions, feel free to try them.
For a few seconds, the optimization is done. Then, we can visualize the optimization progress.

.. code:: python

    import matplotlib.pyplot as plt
    plt.plot(obj.get_history_bestsofar())
    plt.savefig('figure.png')

which looks like

.. image:: https://github.com/eyounx/ZOOpt/blob/dev/img/quick_start.png?raw=true" alt="Expeirment results
   :width: 400px

We can also use ``ExpOpt`` to repeat the optimization for performance analysis, which will calculate the mean and standard deviation of multiple optimization results while automatically visualizing the optimization progress.

.. code:: python

    solution_list = ExpOpt.min(obj, Parameter(budget=100*dim), repeat=3, plot=True, plot_file="progress.png")
    for solution in solution_list:
        print(solution.get_x(), solution.get_value())

More examples are available in the **Example** part.
