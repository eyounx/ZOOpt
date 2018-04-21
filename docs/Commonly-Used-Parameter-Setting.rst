---------------------------------
Commonly Used Parameters Setting
---------------------------------
In ZOOclient, The type ``Parameter`` defines all parameters used in the
optimization algorithms. Commonly, five parameters are needed to be
manually determined by users. Respectively are ``budget``,
``evaluation_server_num``, ``control_server_ip_port``,
``objective_file`` and ``func``.

.. code:: julia

    par = Parameter(budget=10000, evaluation_server_num=10, control_server_ip_port="192.168.1.105:20000",
    objective_file="fx.py", func="ackley")

-  ``budget`` means the number of calls to the objective function.
-  ``evaluation_server_num`` is the number of evaluation servers client
   requires.
-  ``control_server_ip_port`` is the control server's ip:port.
-  ``objective_file`` is the file containing the objective funtion.
-  ``func`` is the name of the objective function

The default algorithm used in ZOOclient is ``ASRacos`` (Asynchronous
Sequential Racos). To use ``PPOSS`` method(Parallel Pareto Optimization
for Subset Selection, IJCAI'16), the other method implemented in
ZOOclient, the parameter\ ``constraint="constraint_function_name"`` is
needed and the constraint function should be defined in
``objective_file`` as well.

.. code:: julia

    par = Parameter(budget=10000, evaluation_server_num=10, control_server_ip_port="192.168.1.105:20000",
    objective_file="sparse_mse.py", func="target_func")

Optional Parameters
-------------------

1. ``init_sample``

::

      init_set = [Solution(x = [...]), Solution(x = [...]), ...]
      par = Parameter(..., init_sample=init_set, ...)

In some cases, users don't want to start the optimization from scratch.
``init_sample`` parameter is set for initiatial sample used by
ZOOclient. Some known good solutions can be added in this set. The
number of the solutions is unlimited.

2. ``show_x``

``par = Parameter(..., show_x=true, ...)``

If ``show_x`` is set to true, ZOOclient will print the best solution's x
as well as value every 10 seconds. Otherwise, best solution's x will not
be printed.

3. ``output_file``

``par = Parameter(..., output_file="log.txt", ...)``

If ``output_file`` is set, ZOOclient will output the the best solution's
value every 10 seconds to this file. If ``show_x`` is true, best
solution's x is also be output.
