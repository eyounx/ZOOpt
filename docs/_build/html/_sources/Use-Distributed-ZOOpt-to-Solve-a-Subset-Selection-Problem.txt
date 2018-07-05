----------------------------------------------------------
Use Distributed ZOOpt to Solve a Subset Selection Problem
----------------------------------------------------------
Subset selection that selects a few variables from a large set is a
fundamental problem in many areas. The recently emerged Pareto
Optimization for Subset Selection (POSS) method is a powerful
approximation solver for this problem. Its parallel version PPOSS,
proved to have good properties for parallelization while preserving the
approximation quality, is implemented in
`ZOOclient <https://github.com/eyounx/ZOOjl.jl>`__.

Sparse regression can be expressed as a subset selection problem. For
sparse regression, the objective is to learn a linear classifier *w*
minimzing the mean squared error, while the number of non-zero elements
of *w* should be not larger than *k*, which is a sparsity requirement.
The objective function can be write as
``min_w mse(w)   s.t.  ||w||_0 <= k``

The process to start the control server and evaluation servers are
omitted in this example. We define a sparse regression problem in
`ZOOsrv <https://github.com/eyounx/ZOOsrv>`__
``example/objective_function`` fold and use the data set ``sonar`` to
test the performance. Notice that to use PPOSS method, users should
define the objective funtion together with the constraint function.

.. code:: python

    mse = SparseMSE('objective_function/data/sonar.arff')
    mse.set_sparsity(8)

    def loss(solution):
        return mse.loss(solution)

    def constraint(solution):
        return mse.constraint(solution)

Then, write the Julia code and run `this
file <https://github.com/eyounx/ZOOjl.jl/blob/master/example/subsetsel_client.jl>`__.

    subsetsel\_client.jl

.. code:: julia

    using ZOOclient
    using PyPlot

    # define a Dimension object
    dim_size = 60
    dim_regs = [[0, 1] for i = 1:dim_size]
    dim_tys = [false for i = 1:dim_size]
    mydim = Dimension(dim_size, dim_regs, dim_tys)
    # define an Objective object
    obj = Objective(mydim)

    # define a Parameter Object
    # budget:  the number of calls to the objective function
    # evalueation_server_num: the number of evaluation servers
    # control_server_ip_port: the ip:port of the control server
    # objective_file: the objective funtion is defined in this file
    # func: the name of the objective function
    # constraint: the name of the constraint function
    par = Parameter(budget=1000, evaluation_server_num=2, control_server_ip_port="192.168.1.105:20000",
        objective_file="sparse_mse.py", func="loss", constraint="constraint")

    # perform optimization
    sol = zoo_min(obj, par)
    # print the Solution object
    sol_print(sol)

    # visualize the optimization progress
    history = get_history_bestsofar(obj)
    plt[:plot](history)
    plt[:savefig]("figure.pdf")

An extra parameter ``constraint="constraint_function_name"`` should be
set in the definition of the ``Parameter`` object.

Finally, type the following command

::

    $ ./julia -p 4 /path/to/your/directory/subsetsel_clinet.jl

For a few seconds, the optimization is done and we will get the result.

.. image:: https://github.com/eyounx/ZOOjl/blob/master/img/sparse_mse_result.png?raw=true
Visualized optimization progress looks like:

.. image:: https://github.com/eyounx/ZOOjl/blob/master/img/sparse_mse.png?raw=true
    :width: 500
​
