---------------------------------------------------------------------------------
How to Optimize a Function with the Mixed (Continuous and Discrete) Search Space
---------------------------------------------------------------------------------
In some cases, the search space of the problem consists of both
continuous subspace and discrete subspace. ZOOpt can solve this kind of
problem easily.

We define the Sphere function in simple\_function.py for minimization.

.. code:: python

    def sphere_mixed(solution):
        """
        Sphere function for mixed optimization
        """
        x = solution.get_x()
        value = sum([i*i for i in x])
        return value

Then, define corresponding *objective* and *parameter*.

.. code:: python

    dim_size = 100
    dim_regs = []
    dim_tys = []
    # In this example, the search space is discrete if this dimension index is odd, Otherwise, the search space is continuous.
    for i in range(dim_size):
        if i % 2 == 0:
            dim_regs.append([0, 1])
            dim_tys.append(True)
        else:
            dim_regs.append([0, 100])
            dim_tys.append(False)
    dim = Dimension(dim_size, dim_regs, dim_tys)
    objective = Objective(sphere_mixed, dim)  # form up the objective function

.. code:: python

    budget = 100 * dim_size  # number of calls to the objective function
    parameter = Parameter(budget=budget)

Finally, use ZOOpt to optimize.

.. code:: python

    solution_list = ExpOpt.min(objective, parameter, repeat=1, plot=True)

The whole process lists below.

.. code:: python

    from simple_function import sphere_mixed
    from zoopt import Dimension, Objective, Parameter, ExpOpt


    # mixed optimization
    def minimize_sphere_mixed():
        """
        Mixed optimization example of minimizing sphere function, which has mixed search search space.

        :return: no return value
        """

        # setup optimization problem
        dim_size = 100
        dim_regs = []
        dim_tys = []
        # In this example, the search space is discrete if this dimension index is odd, Otherwise, the search space
        # is continuous.
        for i in range(dim_size):
            if i % 2 == 0:
                dim_regs.append([0, 1])
                dim_tys.append(True)
            else:
                dim_regs.append([0, 100])
                dim_tys.append(False)
        dim = Dimension(dim_size, dim_regs, dim_tys)
        objective = Objective(sphere_mixed, dim)  # form up the objective function
        budget = 100 * dim_size  # the number of calls to the objective function
        parameter = Parameter(budget=budget)

        solution_list = ExpOpt.min(objective, parameter, repeat=1, plot=True)

    if __name__ == '__main__':
        minimize_sphere_mixed()

For a few seconds, the optimization is done. Visualized optimization
progress looks like

.. image:: https://github.com/eyounx/ZOOpt/blob/dev/img/sphere_mixed_figure.png?raw=true

More concrete examples are available in the
``example/simple_functions/mixed_opt.py`` file .
