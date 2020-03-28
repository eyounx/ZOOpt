Parameters in ZOOpt
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

With the aim of supporting machine learning tasks, ZOOpt includes a
set of methods that are efficient and performance-guaranteed, with addons handling noise and high-dimensionality. This page explains how to use these methods via setting appropriate parameters.

.. contents:: Table of Contents

Parameters in ``Dimension``, ``Objective`` and ``Parameter``
------------------------------------------------------------

To handle different tasks, users are to set specific parameters in
``Dimension`` (or ``Dimension2``), ``Objective`` and ``Parameter`` objects. Constructors of
these classes are listed here for looking up. This part can be skipped
if you don't want to know all details of the parameters in these
classes.

Dimension
>>>>>>>>>>

.. code:: python

    class Dimension:
        """
        This class describes dimension information of the search space.
        """
         def __init__(self, size=0, regs=[], tys=[], order=[]):

-  ``size`` is an integer indicating the dimension size.
-  ``regs`` is a list contains the search space of each dimension
   (search space is a two-element list showing the range of each
   dimension, e.g., [-1, 1] for the range from -1 to 1, including -1 and 1).
-  ``tys`` is a list of boolean value, ``True`` means continuous in this
   dimension and ``False`` means discrete.
-  ``order`` is a list of boolean value, ``True`` means this dimension
   has an order relation and ``False`` means not. The boolean
   value in ``order`` is effective only when this dimension is discrete.
   By default, ``order=[False] * size``. Setting ```order`` for discrete optimization
   problems which have ordered relations in their search space, can increase the  optimization
   performance.

Dimension2
>>>>>>>>>>

.. code:: python

    class Dimension2:
        """
        This class is another format to describe dimension information of the search space.
        """
         def __init__(self, dim_list=[]):

-  ``dim_list`` is a list of tuples.Each tuple has three arguments. For continuous dimensions, arguments are
   ``(type, range, float_precision)``. ``type`` indicates the continuity of the dimension,
   which should be set to ``ValueType.CONTINUOUS``. ``range`` is a list that indicates the search space.
   ``float_precision`` indicates the precision of the dimension, e.g., if ``float_precision``
   is set to ``1e-6``, ``0.001``, or ``10``, the answer will be accurate to six decimal places,
   three decimal places, or tens places. For discrete dimensions, arguments are
   ``(type, range, has_partial_order)``. ``type`` indicates the continuity of the dimension,
   which should be set to ``ValueType.DISCRETE``. ``range`` is a list that indicates the search space.
   ``has_partial_order`` indicates whether this dimension is ordered. ``True`` is for an ordered
   relation and ``False`` means not.

Objective
>>>>>>>>>>

.. code:: python

    class Objective:
        """
        This class represents the objective function and its associated variables
        """
        def __init__(self, func=None, dim=None, constraint=None, resample_func=None):

-  ``func`` is the objective function to be optimized. Indispensable
   parameter for all tasks.
-  ``dim`` is a ``Dimension`` (or ``Dimension2``) object describing information of the
   search space. Indispensable parameter for all tasks.
-  ``constraint`` is set for subset selection algorithm ``POSS``.
   Optional parameter.
-  ``resample_func`` and ``balance_rate`` is set for ``SSRACOS``, a
   noise handling variant of general optimization method ``SRACOS``.
   Optional parameters.

Parameter
>>>>>>>>>>

.. code:: python

    class Parameter:
        """
            This class contains all parameters used for optimization.
        """
        def __init__(self, algorithm=None, budget=0, exploration_rate=0.01, init_samples=None, time_budget=None, terminal_value=None,                   sequential=True, precision=None, uncertain_bits=None, intermediate_result=False, intermediate_freq=100, autoset=True,
                     noise_handling=False, resampling=False, suppression=False, ponss=False, ponss_theta=None, ponss_b=None,
                     non_update_allowed=500, resample_times=100, balance_rate=0.5, high_dim_handling=False, reducedim=False, num_sre=5,
                     low_dimension=None, withdraw_alpha=Dimension(1, [[-1, 1]], [True]), variance_A=None,
                     stopping_criterion=DefaultStoppingCriterion(), seed=None, parallel=False, server_num=1):

-  ``budget`` is the only indispensable parameter of all tasks, it means
   the number of calls to the objective function.
-  ``autoset`` is ``True`` by default. If ``autoset=False``, users
   should control all the algorithm parameters.
-  ``algorithm`` is the optimization algorithm that ZOOpt uses, can be
   'racos' or 'poss'. By default it is set to 'racos'. When the solution
   space is binary and a constraint function has been set, the default
   algorithm is 'poss'.
-  ``init_samples`` is a list of samples (``Solution`` objects) provided
   by user. By default it is ``None`` and the algorithm will randomly
   sample initial solutions. If the users do have some initial samples,
   set the samples to ``init_samples``, and these samples will be added
   into the first sampled solution set.
-  ``time_budget`` set the time limit of the optimization algorithm. If
   running time exceeds this value, the optimization algorithm will
   return the best solution immediately.
-  ``terminal_value`` is set for early stop. The optimization procedure
   will stop if the function value reaches ``terminal_value``
-  ``sequential`` switches between ``RACOS`` and ``SRACOS`` optimization
   algorithms. ``sequential`` equals to ``True`` by default and ZOOpt
   will use ``SRACOS``. Otherwise, ZOOpt will use ``RACOS``.
-  ``precision`` sets the precision of the result.
-  ``uncertain_bits`` sets the number of uncertain bits in ``RACOS``,
   ``SRACOS``, and ``SSRACOS``.
-  ``intermediate_result`` and ``intermediate_freq`` are set for showing
   intermediate results during the optimization progress. The procedure
   will show the best solution every ``intermediate_freq`` calls to the
   objective function if ``intermediate_result=True``.
-  ``noise_handling``, ``resampling``, ``suppression``, ``ponss``,
   ``ponss_theta``, ``ponss_b``, ``non_update_allowed``,
   ``resample_times``, ``balance_rate`` are set for noise handling.
-  ``high_dim_handling``, ``reducedim``, ``num_sre``, ``low_dimension``,
   ``withdraw_alpha``, ``variance_A`` are set for high-dimensionality
   handling. Details of parameter setting for noise handling and
   high-dimensionality handling in ZOOpt will be discussed in the next
   part.
-  ``stopping_criterion`` sets a stopping criterion for the optimization. It should be  an instance of a 
   class that implements the   member function ``check(self, optcontent)``, which will be invoked at each iteration of the optimization. The optimization algorithm will  stop in advance if ``stopping_criterion.check()`` returns True.
-  ``seed`` sets the seed of all generated random numbers used in ZOOpt.
-  ``parallel`` and ``server_num`` are set for parallel optimization.



Parameter settings in different tasks
-----------------------------------------

We will introduce the most important parameter settings in different tasks and
omit the others.

Optimize a function with the continuous search space
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

A ``Dimension`` object should be paid attention to in this example.
``ty`` of the ``Dimension`` object should be set ``[True] * dim_size``,
which means it's search space is continuous.

.. code:: python

    dim_size = 10
    dim = Dimension(dim_size, [[-1, 1]] * dim_size, [True] * dim_size)
    # dim = Dimension2([(ValueType.CONTINUOUS, [-1, 1], 1e-6)] * dim_size)

Optimize a function with the discrete search space
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

In this example, ``ty`` of the ``Dimension`` object should be set
``[False] * dim_size``, which means it's search space is discrete.

.. code:: python

    dim_size = 10
    dim = Dimension(dim_size, [[-1, 1]] * dim_size, [False] * dim_size)
    # dim = Dimension2([(ValueType.DISCRETE, [-1, 1], False)] * dim_size)

If the search space of a dimension is discrete and has partial order
relation, ``order`` of this dimension should be set to ``True``.

.. code:: python

    dim_size = 10
    dim = Dimension(dim_size, [[-1, 1]] * dim_size, [False] * dim_size, [True] * dim_size)
    # dim = Dimension2([(ValueType.DISCRETE, [-1, 1], True)] * dim_size)

Optimize a function with the mixed search space
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

In this example, the search space is mixed with continuous subspace and
discrete subspace.

.. code:: python

    dim = Dimension(3, [[-1, 1]] * 3, [False, False, True], [False, True, False])
    # dim = Dimension2([(ValueType.DISCRETE, [-1, 1], False),
    #                   (ValueType.DISCRETE, [-1, 1], True),
    #                   (ValueType.CONTINUOUS, [-1, 1], 1e-6)])

It means the dimension size is 3, the range of each dimension is [-1,
1]. The first dimension is discrete and does not have partial order
relation. The second dimension is discrete and has partial order
relation. The third dimension is continuous.

Optimize a noisy function
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

Three noise handling methods are implemented in ZOOpt, respectively are
resampling, value suppression for ``SRACOS`` (``SSRACOS``) and threshold
selection for ``POSS`` (``PONSS``).

Resampling
::::::::::::

Resamping is a generic nosie handling method of all optimization
algorithms. It evalueates one sample several times to obtain a stable
mean value.

.. code:: python

    parameter = Parameter(budget=100000, noise_handling=True, resampling=True, resample_times=10)

To use resampling in ZOOpt, ``noise_handling`` and ``resampling`` should
be set to ``True``. ``resample_times``, times of evaluating one sample,
should also be provided by users.

Value Suppression for ``SRACOS`` (``SSRACOS``)
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

Value suppression is a noise handling method proposed recently.

.. code:: python

    parameter = Parameter(budget=100000, noise_handling=True, suppression=True, non_update_allowed=500, resample_times=100, balance_rate=0.5)

To use ``SSRACOS`` in ZOOpt, ``noise_handling`` and ``suppression``
should be set to ``True``. ``non_update_allowed``, ``resample_times``
and ``balance_rate`` should be provided by users. It means if the best
solution doesn't change for ``non_update_allowed`` budgets, the best
solution will be re-evaluated for ``resample_times`` times.
``balance_rate`` is a parameter for exponential weight average of
several evaluations of one sample.

Threshold Selection for ``POSS`` (``PONSS``)
::::::::::::::::::::::::::::::::::::::::::::::::

``PONSS`` is a variant of ``POSS`` and designed to solve noisy subset
selection problems.

.. code:: python

    parameter = Parameter(budget=20000, algorithm='poss', noise_handling=True, ponss=True, ponss_theta=0.5, ponss_b=8)

To use ``PONSS`` in ZOOpt, ``noise_handling`` and ``ponss`` should be
set to ``True``. ``ponss_theta`` and ``ponss_b`` are parameters used in
``PONSS`` algorithm and should be provided by users. ``ponss_theta``
stands for the threshold. ``ponss_b`` limits the number of solutions in
the population set.

Optimize a high-dimensionality function
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

ZOOpt implements a high-dimensionality handling method called sequential
random embedding (``SRE``).

.. code:: python

    parameter = Parameter(budget=100000, high_dim_handling=True, reducedim=True, num_sre=5, low_dimension=Dimension(10, [[-1, 1]] * 10, [True] * 10))

To use ``SRE`` in ZOOpt, ``high_dim_handling`` and ``reducedim`` should
be set to ``True``. ``num_sre``, ``low_dimension`` and
``withdraw_alpha`` are parameters used in ``SRE`` and should be provided
by users. ``num_sre`` means the number of sequential random embedding.
``low_dimension`` stands for the low dimension ``SRE`` projects to.
``withdraw_alpha`` and ``variance_A`` are optional parameters.
``withdraw_alpha``, a withdraw variable to the previous solution, is a
``Dimension`` object with only one dimension. ``variance_A`` specifies
the variance of the projection matrix A. By default, ``withdraw_alpha``
equals to ``Dimension(1, [[-1, 1]], [True])`` and ``variance_A`` equals
to ``1/d`` (``d`` is the dimension size of the ``low_dimension``). In
most cases, it's not necessary for users to provide them.
