---------------------------------
How to Optimize a Noisy Function
---------------------------------
Many real-world environments are noisy, where solution evaluations are
inaccurate due to the noise. Noisy evaluation can badly injure
derivative-free optimization, as it may make a worse solution looks
better.

Three noise handling methods are implemented in ZOOpt, respectively are
resampling, value suppression for ``SRACOS`` (``SSRACOS``) and threshold
selection for ``POSS`` (``PONSS``).

In this page, we provide examples of how to use the three noise handling
methods in ZOOpt.

Re-sampling and Value Suppression
---------------------------------

We define the Ackley function under noise in simple\_function.py for
minimization.

.. code:: python

    import numpy as np

    def ackley(solution):
        """
        Ackley function for continuous optimization
        """
        x = solution.get_x()
        bias = 0.2
        ave_seq = sum([(i - bias) * (i - bias) for i in x]) / len(x)
        ave_cos = sum([np.cos(2.0*np.pi*(i-bias)) for i in x]) / len(x)
        value = -20 * np.exp(-0.2 * np.sqrt(ave_seq)) - np.exp(ave_cos) + 20.0 + np.e
        return value


    def ackley_noise_creator(mu, sigma):
        """
        Ackley function under noise
        """
        return lambda solution: ackley(solution) + np.random.normal(mu, sigma, 1)

Then, define a corresponding *objective* object.

.. code:: python

    ackley_noise_func = ackley_noise_creator(0, 0.1)
    dim_size = 100  # dimensions
    dim_regs = [[-1, 1]] * dim_size  # dimension range
    dim_tys = [True] * dim_size  # dimension type : real
    dim = Dimension(dim_size, dim_regs, dim_tys)  # form up the dimension object
    objective = Objective(ackley_noise_func, dim)  # form up the objective function

Re-sampling
~~~~~~~~~~~

To use Re-sampling noise handling method, ``noise_handling`` and
``resampling`` should be set to ``True``. In addition,
``resample_times`` should be provided by users.

.. code:: python

    parameter = Parameter(budget=200000, noise_handling=True, resampling=True, resample_times=10)
    # This setting is alternative
    parameter.set_positive_size(5)

Value Suppression for ``SRACOS`` (``SSRACOS``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To use ``SSRACOS`` noise handling method, ``noise_handling`` and
``suppression`` should be set to ``True``. In addition,
``non_update_allowed``, ``resample_times`` and ``balance_rate`` should
be provided by users.

.. code:: python

    # non_update_allowed=500 and resample_times=100 means if the best solution doesn't change for 500 budgets, the best solution will be evaluated repeatedly for 100 times
    # balance_rate is a parameter for exponential weight average of several evaluations of one sample.
    parameter = Parameter(budget=200000, noise_handling=True, suppression=True, non_update_allowed=500, resample_times=100, balance_rate=0.5)
    # This setting is alternative
    parameter.set_positive_size(5)

Finally, use ``ExpOpt.min`` to optimize this function.

.. code:: python

    solution_list = ExpOpt.min(objective, parameter, repeat=1, plot=True)

Threshold Selection for ``POSS`` (``PONSS``)
--------------------------------------------

A sparse regression problem is defined in
``example/sparse_regression/sparse_mse.py`` .

Then define a corresponding *objective* object.

.. code:: python

    from sparse_mse import SparseMSE
    from zoopt import Objective, Parameter, ExpOpt
    from math import exp

    # load data file
    mse = SparseMSE('sonar.arff')
    mse.set_sparsity(8)

    # setup objective
    objective = Objective(func=mse.loss, dim=mse.get_dim(), constraint=mse.constraint)

To use ``PONSS`` noise handling method, ``algorithm`` should be set to
``'poss'`` and ``noise_handling``, ``ponss`` should be set to ``True``.
In addition, ``ponss_theta`` and ``ponss_b`` should be provided by
users.

.. code:: python

    # ponss_theta and ponss_b are parameters used in PONSS algorithm and should be provided by users. ponss_theta stands
    # for the threshold. ponss_b limits the number of solutions in the population set.
    parameter = Parameter(algorithm='poss', noise_handling=True, ponss=True, ponss_theta=0.5, ponss_b=mse.get_k(),
                              budget=2 * exp(1) * (mse.get_sparsity() ** 2) * mse.get_dim().get_size())

Finally, use ``ExpOpt.min`` to optimize this function.

.. code:: python

    solution_list = ExpOpt.min(objective, parameter, repeat=1, plot=True)

More concrete examples are available in the
``example/simple_functions/opt_under_noise.py`` and
``example/sparse_regression/ponss_opt.py``.
