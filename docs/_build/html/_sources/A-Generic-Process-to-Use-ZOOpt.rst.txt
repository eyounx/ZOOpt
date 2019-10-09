--------------------------------
A Generic Process to Use ZOOpt
--------------------------------

A Brief Introduction to ZOOpt Components
----------------------------------------

In ZOOpt, an optimization problem is abstracted in several components:
``Objective``, ``Dimension``, ``Parameter``, and ``Solution``, each is a
Python class.

An ``Objective`` object is initialized with a function and a
``Dimension`` object as the input, where the ``Dimension`` object
defines the dimension size and boundaries of the search space. A
``Parameter`` object specifies algorithm parameters. ZOOpt is able to
automatically choose parameters for a range of problems, leaving only
one parameter of the optimization budget (i.e. the number of solution
evaluations) needed to be manually determined according to the time of
the user. The ``Opt.min`` function makes the optimization happen, and
returns a ``Solution`` object which contains the final solution and the
function value. Moreover, after the optimization, the ``Objective``
object contains the history of the optimization for observation.

A Generic Process to Use ZOOpt
------------------------------

The Generic process to use ZOOpt contains four steps

-  Define an objective function ``f``
-  Define a ``Dimension`` object ``dim``, then use ``f`` and ``dim`` to
   construct an ``Objective`` object
-  Define a ``Parameter`` object ``par``
-  Use ``Opt.min`` or ``ExpOpt.min`` to optimize

Details of the Generic Process
------------------------------

Define objective function
~~~~~~~~~~~~~~~~~~~~~~~~~

An objective function should satisfy the interface
``def func(solution):`` , where ``solution`` is a ``Solution`` object
which encapsulates x and f(x). In general, users can custom their
objective function by

.. code:: python

    def func(solution):
        x = solution.get_x() # fixed pattern
        value = f(x) # function f takes a vector x as input
        return value

In the Sphere function example, the objective function looks like

.. code:: python

    def sphere(solution):
        x = solution.get_x()
        value = sum([(i-0.2)*(i-0.2) for i in x]) # sphere center is (0.2, 0.2)
        return value

The objective function can also be a member function of a class, so that
it can be much more complex than a singleton function. In this case, the
function should satisfy the interface ``def func(self, solution):``.

Define ``Dimension`` object ``dim``, then use ``f`` and ``dim`` to construct an ``Objective`` object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A ``Dimension`` object ``dim`` and an objective function ``f`` are
necessary components to construct an ``Objective`` object, which is one
of the two requisite parameters to call ``Opt.min`` function.

``Dimension`` class has an initial function looks like

.. code:: python

    def __init__(self, size=0, regs=[], tys=[], order=[]):

``size`` is an integer indicating the dimension size. ``regs`` is a list
contains the search space of each dimension (search space is a
two-element list showing the range of each dimension, e.g., [-1, 1] for
the range from -1 to 1). ``tys`` is a list of boolean value, ``True``
means continuous in this dimension and ``False`` means discrete.
``order`` is a list of boolean value, ``True`` means this dimension has
a partial order relation and ``False`` means not. The boolean value in
``order`` is effective only when this dimension is discrete. By default,
``order=[False] * size``. In most cases, ``order`` is not a necessity.

In the Sphere function example, ``dim`` looks like

.. code:: python

    dim_size = 100
    dim = Dimension(dim_size, [[-1, 1]] * dim_size, [True] * dim_size )

It means that the dimension size is 100, the range of each dimension is
[-1, 1] and is continuous.

Then use ``dim`` and ``f`` to construct an Objective object.

.. code:: python

    objective = Objective(sphere, dim)

Define ``parameter`` objective ``par``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The class ``Parameter`` defines all parameters used in the optimization
algorithms. Commonly, ``budget`` is the only parameter needed to be
manually determined by users, while all parameters are controllable.
Other parameters will be discussed in `Commonly used parameter setting
in ZOOpt `

.. code:: python

    par = Parameter(budget=10000)

Use ``Opt.min`` or ``ExpOpt.min`` to optimize
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Opt.min`` and ``ExpOpt.min`` are two interfaces for optimization.

``Opt.min`` takes an ``Objective`` object e.g. ``objective`` and a
``Parameter`` object e.g. ``par`` as input. It will return a
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
        def min(objective, parameter, repeat=1, best_n=None, plot=False, plot_file=None, seed=None):

``repeat`` indicates the number of repetitions of the optimization (each
starts from scratch). ``best_n`` is a parameter for result analysis,
``best_n`` is an integer and equals to ``repeat`` by default.
``ExpOpt.min`` will print the average value and the standard deviation
of the ``best_n`` best results among the returned solution list.
``plot`` determines whether to plot the regret curve on screen during
the optimization progress. When ``plot=True``, the procedure will be
blocked and show figure during its running if ``plot_file`` is not
given. Otherwise, the procedure will save the figures to disk without
blocking. ``seed`` is a parameter to set random seed in optimization.

.. code:: python

    solution_list = ExpOpt.min(objective, par, repeat=10, best_n=5, plot=True, plot_file='opt_progress.pdf', seed=777)
