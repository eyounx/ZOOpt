--------------------------------------
How to Optimize a Discrete Function
--------------------------------------

The `set cover <https://en.wikipedia.org/wiki/Set_cover_problem>`__
problem is a classical question in combinatorics, computer science and
complexity theory. It is one of Karp's 21 NP-complete problems shown to
be NP-complete in 1972.

We define the SetCover function in fx.py for minimization.

.. code:: python

    from zoopt.dimension import Dimension

    class SetCover:
        """
        set cover problem for discrete optimization
        this problem has some extra initialization tasks, thus we define this problem as a class
        """
        __weight = None
        __subset = None

        def __init__(self):
            self.__weight = [0.8356, 0.5495, 0.4444, 0.7269, 0.9960, 0.6633, 0.5062, 0.8429, 0.1293, 0.7355,
                             0.7979, 0.2814, 0.7962, 0.1754, 0.0267, 0.9862, 0.1786, 0.5884, 0.6289, 0.3008]
            self.__subset = []
            self.__subset.append([0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0])
            self.__subset.append([0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0])
            self.__subset.append([1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0])
            self.__subset.append([0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0])
            self.__subset.append([1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1])
            self.__subset.append([0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0])
            self.__subset.append([0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0])
            self.__subset.append([0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0])
            self.__subset.append([0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0])
            self.__subset.append([0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1])
            self.__subset.append([0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0])
            self.__subset.append([0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1])
            self.__subset.append([1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1])
            self.__subset.append([1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1])
            self.__subset.append([0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1])
            self.__subset.append([1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0])
            self.__subset.append([1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1])
            self.__subset.append([0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1])
            self.__subset.append([0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0])
            self.__subset.append([0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1])

        def fx(self, solution):
            """
            objective function
            """
            x = solution.get_x()
            allweight = 0
            countw = 0
            for i in range(len(self.__weight)):
                allweight += self.__weight[i]

            dims = []
            for i in range(len(self.__subset[0])):
                dims.append(False)

            for i in range(len(self.__subset)):
                if x[i] == 1:
                    countw += self.__weight[i]
                    for j in range(len(self.__subset[i])):
                        if self.__subset[i][j] == 1:
                            dims[j] = True
            full = True
            for i in range(len(dims)):
                if dims[i] is False:
                    full = False

            if full is False:
                countw += allweight

            return countw

        @property
        def dim(self):
            """
            Dimension of set cover problem.
            :return: Dimension instance
            """
            dim_size = 20
            dim_regs = [[0, 1]] * dim_size
            dim_tys = [False] * dim_size
            return Dimension(dim_size, dim_regs, dim_tys)

Then, Define corresponding *objective* and *parameter*.

.. code:: python

    problem = SetCover()
    dim = problem.dim  # the dim is prepared by the class
    objective = Objective(problem.fx, dim)  # form up the objective function

.. code:: python

    # autoset=True in default. If autoset is False, you should define train_size, positive_size, negative_size on your own.
    parameter = Parameter(budget=budget, autoset=False)
    parameter.set_train_size(6)
    parameter.set_positive_size(1)
    parameter.set_negative_size(5)

Finally, optimize this function.

.. code:: python

    ExpOpt.min(objective, parameter, repeat=1, plot=True)

The whole process lists below.

.. code:: python

    from fx import SetCover
    from zoopt import Dimension, Objective, Parameter, ExpOpt


    def minimize_setcover_discrete():
        """
        Discrete optimization example of minimizing setcover problem.
        """
        problem = SetCover()
        dim = problem.dim  # the dim is prepared by the class
        objective = Objective(problem.fx, dim)  # form up the objective function

        budget = 100 * dim.get_size()  # number of calls to the objective function
        # if autoset is False, you should define train_size, positive_size, negative_size on your own
        parameter = Parameter(budget=budget, autoset=False)
        parameter.set_train_size(6)
        parameter.set_positive_size(1)
        parameter.set_negative_size(5)

        ExpOpt.min(objective, parameter, repeat=1, plot=True)

    if __name__ == '__main__':
        minimize_setcover_discrete()

For a few seconds, the optimization is done. Visualized optimization
progress looks like

.. image:: https://github.com/eyounx/ZOOpt/blob/dev/img/setcover_discrete_figure.png?raw=true
    :width: 500

More concrete examples are available in the
``example/simple_functions/discrete_opt.py`` file.
