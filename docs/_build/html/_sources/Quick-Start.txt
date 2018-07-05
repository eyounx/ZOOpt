---------------
Quick Start
---------------
ZOOpt is a python package of `Zeroth-Order
Optimization <https://github.com/eyounx/ZOOpt/wiki/Derivative-Free-Optimization>`__.

Required packages
-----------------

This package requires the following packages:

-  Python version 2.7 or 3.5
-  ``numpy`` http://www.numpy.org
-  ``matplotlib`` http://matplotlib.org/ (optional for plot drawing)

The easiest way to get these is to use
`pip <https://pypi.python.org/pypi/pip>`__ or
`conda <https://www.anaconda.com/what-is-anaconda/>`__ environment
manager. Typing the following command in your terminal will install all
required packages in your Python environment.

::

    $ conda install numpy matplotlib

or

::

    $ pip install numpy matplotlib

Getting and installing ZOOpt
----------------------------

The easiest way to get ZOOpt is to type ``pip install zoopt`` in you
terminal/command line.

If you want to install ZOOpt by source code, download this project and
sequentially run following commands in your terminal/command line.

::

    $ python setup.py build
    $ python setup.py install

A quick example
---------------

We define the Ackley function for minimization (note that this function
is for arbitrary dimensions, determined by the solution)

.. code:: python

    def ackley(solution):
        """Ackley function for continuous optimization"""
        x = solution.get_x()
        bias = 0.2
        ave_seq = sum([(i - bias) * (i - bias) for i in x]) / len(x)
        ave_cos = sum([np.cos(2.0 * np.pi * (i - bias)) for i in x]) / len(x)
        value = -20 * np.exp(-0.2 * np.sqrt(ave_seq)) - np.exp(ave_cos) + 20.0 + np.e
        return value

Ackley function is a classical function with many local minima. In
2-dimension, it looks like (from wikipedia)

.. image:: https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Ackley%27s_function.pdf/page1-400px-Ackley%27s_function.pdf.jpg?raw=true

We then use ZOOpt to optimize a 100-dimension Ackley function:

1. import components from zoopt, where ``ExpOpt`` is the
   experiment-purpose replacement of ``Opt``

.. code:: python

    from zoopt import Dimension, Objective, Parameter, ExpOpt

2. set the dimension

.. code:: python

    dim = 100  # dimension

3. set up the ``Dimension`` object

.. code:: python

    # The search space is [-1, 1] for each dimension and is continuous 
    dimobj = Dimension(dim, [[-1, 1]] * dim, [True] * dim)

4. set up the ``Objective`` object defining the function to be minimized

.. code:: python

    objective = Objective(ackley, dimobj)

5. set up the parameters of the optimization algorithms. The minimum
   variable is the budget size

.. code:: python

    parameter = Parameter(budget=100 * dim)

6. perform the optimization by

.. code:: python

    solution = Opt.min(objective, parameter)

7. visualize the optimization progress

.. code:: python

    import matplotlib.pyplot as plt

    plt.plot(objective.get_history_bestsofar())
    plt.savefig('opt_progress.pdf')

Combining step 6 and 7, ``ExpOpt`` (from v0.2) can be used for experiments, which supports multi-repeat and ploting

.. code:: python

    solution_list = ExpOpt.min(objective, parameter, repeat=1, plot=True, plot_file='opt_progress.pdf')
   
Finally the whole piece of the code for optimization is:

.. code:: python

   from zoopt import Dimension, Objective, Parameter, ExpOpt

   if __name__ == '__main__':
          dim = 100 # dimension
          Objective(ackley, Dimension(dim, [[-1, 1]] * dim, [True] * dim)) #set up objective
          parameter = Parameter(budget=100 * dim)
          solution_list = ExpOpt.min(objective, parameter, repeat=1, plot=True, plot_file='opt_progress.pdf')


For a few seconds, the optimization is done. The terminal/command line
will show optimization result

.. image:: https://github.com/eyounx/ZOOpt/blob/dev/img/quick_start_cmd.png?raw=true
    
Visualized optimization progress looks like

.. image:: https://github.com/eyounx/ZOOpt/blob/dev/img/quick_start.png?raw=true
    :width: 500
To get all solutions in solution_list, you can type

.. code:: python

    for solution in solution_list:
        x = solution.get_x()
        value = solution.get_value()
        print(x, value)

The rest of the tutorial introduces more functions of ZOOpt.
