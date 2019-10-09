-------------------------------------------
How to Optimize a High-dimensional Function
-------------------------------------------

Derivative-free optimization methods are suitable for sophisticated
optimization problems, while are hard to scale to high dimensionality
(e.g., larger than 1,000).

ZOOpt contains a high-dimensionality handling algorithm called
sequential random embedding (SRE). SRE runs the optimization algorithms
in the low-dimensional space, where the function values of solutions are
evaluated via the embedding into the original high-dimensional space
sequentially. SRE is effective for the function class that all
dimensions may affect the function value but many of them only have a
small bounded effect, and can scale both RACOS and SRACOS (the main
optimization algorithm in ZOOpt) to 100,000-dimensional problems.

In this page, we will show how to use ZOOpt to optimize a high
dimensional function.

We define a variant of Sphere function in simple\_function.py for
minimization.

.. code:: python

    def sphere_sre(solution):
        """
        Variant of the sphere function. Dimensions except the first 10 ones have limited impact on the function value.
        """
        a = 0
        bias = 0.2
        x = solution.get_x()
        x1 = x[:10]
        x2 = x[10:]
        value1 = sum([(i-bias)*(i-bias) for i in x1])
        value2 = 1/len(x) * sum([(i-bias)*(i-bias) for i in x2])
        return value1 + value2

Then, define corresponding *objective* and *parameter*.

.. code:: python

    # sre should be set True
    objective = Objective(sphere_sre, dim, sre=True)

.. code:: python

    # num_sre, low_dimension, withdraw_alpha should be set for sequential random embedding
    # num_sre means the number of sequential random embedding
    # low dimension means low dimensional solution space
    parameter = Parameter(budget=budget, high_dimensionality_handling=True, reducedim=True, num_sre=5, low_dimension=Dimension(10, [[-1, 1]] * 10, [True] * 10))

Finally, use ZOOpt to optimize.

.. code:: python

    solution_list = ExpOpt.min(objective, parameter, repeat=1, plot=True)

The whole process lists below.

.. code:: python

    from simple_function import sphere_sre
    from zoopt import Dimension, Objective, Parameter, ExpOpt


    def sphere_continuous_sre():
        """
        Example of minimizing high-dimensional sphere function with sequential random embedding.

        :return: no return value
        """

        dim_size = 10000  # dimensions
        dim_regs = [[-1, 1]] * dim_size  # dimension range
        dim_tys = [True] * dim_size  # dimension type : real
        dim = Dimension(dim_size, dim_regs, dim_tys)  # form up the dimension object
        objective = Objective(sphere_sre, dim)  # form up the objective function

        # setup algorithm parameters
        budget = 2000  # number of calls to the objective function
        parameter = Parameter(budget=budget, high_dimensionality_handling=True, reducedim=True, num_sre=5, low_dimension=Dimension(10, [[-1, 1]] * 10, [True] * 10))

        solution_list = ExpOpt.min(objective, parameter, repeat=1, plot=True)

    if __name__ == "__main__":
        sphere_continuous_sre()

For a few seconds, the optimization is done. Visualized optimization
progress looks like

.. image:: https://github.com/eyounx/ZOOpt/blob/dev/img/sphere_continuous_sre.png?raw=true
    :width: 500

More concrete examples are available in the
``example/sequential_random_embedding/continuous_sre_opt.py`` file .
