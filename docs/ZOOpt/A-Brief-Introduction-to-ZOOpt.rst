--------------------------------
A Brief Introduction to ZOOpt
--------------------------------

.. contents:: Table of Contents

ZOOpt Components
----------------------------------------

In ZOOpt, an optimization problem is abstracted into several components:
``Objective``, ``Dimension`` (or ``Dimension2``), ``Parameter``, and ``Solution``, each is a
Python class.

An ``Objective`` object is initialized with a function and a
``Dimension`` (or ``Dimension2``) object, where the ``Dimension`` (or ``Dimension2``) object
defines the dimension size and boundaries of the search space. A
``Parameter`` object specifies algorithm parameters. ZOOpt is able to
automatically choose parameters for a range of problems, leaving only
one parameter, the optimization budget (i.e. the number of solution
evaluations), to be manually determined according to the time of
the user. The ``Opt.min`` (or ``ExpOpt.min``) function makes the optimization happen, and
returns a ``Solution`` object which contains the final solution and the
function value (a solution list for ``ExpOpt``). Moreover, after the optimization, the ``Objective``
object contains the history of the optimization for observation.

Use ZOOpt step by step
------------------------------

Using ZOOpt for your optimization tasks contains four steps

-  Define an objective function ``f``
-  Define a ``Dimension`` (or ``Dimension2``) object ``dim``, then use ``f`` and ``dim`` to
   construct an ``Objective`` object
-  Define a ``Parameter`` object
-  Use ``Opt.min`` or ``ExpOpt.min`` to optimize

Define an objective function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An objective function should be defined to satisfy the interface
``def func(solution):`` , where ``solution`` is a ``Solution`` object
which encapsulates x and f(x). In general, users can customize their
objective function by

.. code:: python

    def func(solution):
        x = solution.get_x() # fixed pattern
        value = f(x) # function f takes a vector x as input
        return value

In the Sphere function example, the objective function which looks like

.. code:: python

    def sphere(solution):
        x = solution.get_x()
        value = sum([(i-0.2)*(i-0.2) for i in x]) # sphere center is (0.2, 0.2)
        return value

The objective function can also be a member function of a class, so that
it can be much more complex than a single function. In this case, the
function should be defined to satisfy the interface ``def func(self, solution):``.

Define a ``Dimension`` (or ``Dimension2``) object ``dim``, then use ``f`` and ``dim`` to construct an ``Objective`` object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A ``Dimension`` (or ``Dimension2``) object ``dim`` and an objective function ``f`` are
necessary components to construct an ``Objective`` object, which is one
of the two requisite parameters to call ``Opt.min`` function.

``Dimension`` class has an initial function looks like

.. code:: python

    def __init__(self, size=0, regs=[], tys=[], order=[]):

``size`` is an integer indicating the dimension size. ``regs`` is a list
contains the search space of each dimension (search space is a
two-element list showing the range of each dimension, e.g., [-1, 1] for
the range from -1 to 1, including -1 and 1). ``tys`` is a list of boolean value, ``True``
means it is continuous in this dimension and ``False`` means discrete.
``order`` is a list of boolean value, ``True`` means this dimension has
an order relation and ``False`` means not. The boolean value in
``order`` is effective only when this dimension is discrete. By default,
``order=[False] * size``. Order is quite important for discrete optimization.  
whereby ZOOpt can make full use of the order relation if it is set to be True.
For example, we can specify ``order=[True] * size`` in the optimization of the Sphere function with discrete search space [-10, 10].

In the optmization of the Sphere function with continuous search space, ``dim`` looks like

.. code:: python

    dim_size = 100
    dim = Dimension(dim_size, [[-1, 1]] * dim_size, [True] * dim_size )

It means that the dimension size is 100, the range of each dimension is
[-1, 1] and is continuous.

Besides, if you prefer to put together the info of each dimension,
``Dimension2`` is a good choice. It looks like:

.. code:: python

    def __init__(self, dim_list=[]):

Where ``dim_list`` is a list of tuples.
Each tuple has three arguments. For continuous dimensions, arguments are
``(type, range, float_precision)``. ``type`` indicates the continuity of the dimension,
which should be set to ``ValueType.CONTINUOUS``. ``range`` is a list that indicates the search space.
``float_precision`` indicates the precision of the dimension, e.g., if ``float_precision``
is set to ``1e-6``, ``0.001``, or ``10``, the answer will be accurate to six decimal places,
three decimal places, or tens places. For discrete dimensions, arguments are
``(type, range, has_partial_order)``. ``type`` indicates the continuity of the dimension,
which should be set to ``ValueType.DISCRETE``. ``range`` is a list that indicates the search space.
``has_partial_order`` indicates whether this dimension is ordered. ``True`` is for an ordered
relation and ``False`` means not.

In the optmization of the Sphere function with continuous search space, ``dim`` looks like

.. code:: python

    dim_size = 100
    one_dim = (ValueType.CONTINUOUS, [-1, 1], 1e-6)
    dim_list = [one_dim] * dim_size
    dim = Dimension2(dim_list)

It means that the dimension size is 100, each dimension is continuous, ranging from -1 to 1,
with two decimal precision.

Then use ``dim`` and ``f`` to construct an Objective object.

.. code:: python

    objective = Objective(sphere, dim)

Define a ``parameter`` objective
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The class ``Parameter`` defines all parameters used in the optimization
algorithms. Commonly, ``budget`` is the only parameter needed to be
manually determined by users, while all parameters are controllable.
Other parameters will be discussed in **Commonly used parameter setting
in ZOOpt**

.. code:: python

    par = Parameter(budget=10000)

Use ``Opt.min`` or ``ExpOpt.min`` to optimize
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Opt.min`` and ``ExpOpt.min`` are two functions for optimization.

``Opt.min`` takes an ``Objective`` object, e.g. ``objective``, and a
``Parameter`` object, e.g. ``par``, as input. It will return a
``Solution`` object e.g. ``sol``, which represents the optimal result of
the optimization problem. ``sol.get_x()`` and ``sol.get_value()`` will
return ``sol``'s x and f(x).

.. code:: python

    sol = Opt.min(objective, par)
    print(sol.get_x(), sol.get_value())

``ExpOpt.min`` is an API designed for repeated experiments, it will
return a ``Solution`` object list containing ``repeat`` solutions.

.. code:: python

    class ExpOpt:
        @staticmethod
        def min(objective, parameter, repeat=1, best_n=None, plot=False, plot_file=None):

``repeat`` indicates the number of repetitions of the optimization (each
starts from scratch). ``best_n`` is a parameter for result analysis,
``best_n`` is an integer and equals to ``repeat`` by default.
``ExpOpt.min`` will print the average value and the standard deviation
of the ``best_n`` best results among the returned solution list.
``plot`` determines whether to plot the regret curve on screen during
the optimization progress. When ``plot=True``, the procedure will be
blocked and show figure during its running if ``plot_file`` is not
given. Otherwise, the procedure will save the figures to disk without
blocking.

.. code:: python

    solution_list = ExpOpt.min(objective, par, repeat=10, best_n=5, plot=True, plot_file='opt_progress.pdf')
