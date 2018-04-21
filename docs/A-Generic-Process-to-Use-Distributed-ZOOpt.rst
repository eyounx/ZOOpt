-------------------------------------------
A Generic Process to Use Distributed ZOOpt
-------------------------------------------

A Brief Introduction to ZOOclient Components
--------------------------------------------

In ZOOclient, an optimization problem is abstracted in several
components: ``Objective``, ``Dimension``, ``Parameter``, and
``Solution``, each is a Julia type.

An ``Objective`` object is initialized with a ``Dimension`` object as
the input, where the ``Dimension`` object defines the dimension size and
boundaries of the search space. A ``Parameter`` object specifies
algorithm parameters. The ``zoo_min`` function makes the optimization
happen, and returns a ``Solution`` object which contains the final
solution and the function value. Moreover, after the optimization, the
``Objective`` object contains the history of the optimization for
observation.

A Generic Process to Use Distributed ZOOpt
------------------------------------------

The Generic process to use Distributed ZOOpt contains five steps:

1. Start the control server
   (`ZOOsrv <https://github.com/eyounx/ZOOsrv>`__)
2. Start the evaluation servers (
   `ZOOsrv <https://github.com/eyounx/ZOOsrv>`__)
3. Define the objective function
4. Run Julia client code (
   `ZOOclient <https://github.com/eyounx/ZOOjl.jl>`__)

-  Define a ``Dimension`` object ``dim``, then uses ``dim`` to construct
   an ``Objective`` object
-  Define a ``Parameter`` object ``par``
-  Use ``zoo_min`` to optimize
-  Run client code

5. Shut down evaluation servers and the control server
   (`ZOOsrv <https://github.com/eyounx/ZOOsrv>`__)

The step 1 and the step 2 can be omitted if the servers have been
started. Commonly the step 4 is executed several times for different
tasks. The step 5 could be executed only when users do not want to run
client code any more.

Users carry out step 1, 2 and 5 on general servers and step 3 and 4 for
specific tasks.

Details of the Generic Process
------------------------------

**Start the control server**


Users should provide a port to start the control server.
::

    from zoosrv import control_server
    # users should provide the port occupied by the control server
    control_server.start(20000)

**Start the evaluation servers**


Users should provide a `configuration
file <https://github.com/eyounx/ZOOsrv/blob/master/example/evaluation_server.cfg>`__
to start the evaluation servers.


::

     from zoosrv import evaluation_server
     evaluation_server.start("evaluation_server.cfg")

configuration file is listed as follows:

::

    [evaluation server]
    shared fold = /path/to/project/ZOOsrv/example/objective_function/
    control server ip_port = 192.168.0.103:20000
    evaluation processes = 10
    starting port = 60003
    ending port = 60020

``shared fold`` indicates the root directory your julia client and
evaluation servers work under. The objective function should be defined
under this directory. ``constrol server's ip_port`` means the address of
the control server. The last three lines state we want to start 10
evaluation processes by choosing 10 available ports from 60003 to 60020.

**Define the objective function**


An objective function should satisfy the interface
``def func(solution):`` , where ``solution`` is a ``Solution`` object
that encapsulates x and f(x). In general, users can custom their
objective function by

::

       def func(solution):
           x = solution.get_x() # fixed pattern
           value = f(x) # function f takes a vector x as input
           return value

In the Sphere function example, the objective function looks like

::

       def sphere(solution):
           x = solution.get_x()
           value = sum([(i-0.2)*(i-0.2) for i in x]) # sphere center is (0.2, 0.2)
           return value

**Run Julia client**


1. Define a ``Dimension`` object ``dim``, then uses ``dim`` to construct
   an ``Objective`` object.

``Dimension`` type looks like

::

    type Dimension
         size::Int64
         regions
         types
     end


``size`` is an integer indicating the dimension size. ``regions`` is a
list that contains the search space of each dimension (search space is a
two-element list showing the range of each dimension, e.g., [-1, 1] for
the range from -1 to 1). ``tys`` is a list of boolean value, ``True``
means continuous in this dimension and ``False`` means discrete.

In the Sphere function example, ``dim`` looks like

::

     dim_size = 100
     dim_regs = [[-1, 1] for i = 1:dim_size]
     dim_tys = [true for i = 1:dim_size]
     mydim = Dimension(dim_size, dim_regs, dim_tys)

Then use ``dim`` to construct an ``Objective`` object.
::

    obj = Objective(mydim)

2. Define a ``Parameter`` object ``par``

The type ``Parameter`` defines all parameters used in the optimization
algorithms. Commonly, five parameters are needed to be manually
determined by users. Respectively are ``budget``,
``evaluation_server_num``, ``control_server_ip_port``,
``objective_file`` and ``func``.

::

     # budget:  the number of calls to the objective function
     # evalueation_server_num: the number of evaluation servers
     # control_server_ip_port: the ip:port of the control server
     # objective_file: the objective funtion is defined in this file
     # func: the name of the objective function
     par = Parameter(budget=10000, evaluation_server_num=10, control_server_ip_port="192.168.1.105:20000",
            objective_file="fx.py", func="sphere")

3. Use ``zoo_min`` to optimize

::

         sol = zoo_min(obj, par)
         # print the Solution object
         sol_print(sol)

4. Run client code

``$ ./julia -p 10 /path/to/your/clent/code/client.jl``

Starting with ``julia -p n`` provides ``n`` worker processes on the
local machine. Generally it makes sense for ``n`` to equal the number of
CPU cores on the machine.

5. Shut down evaluation servers and the control server

The control server process can interact with users. The evaluation
processes should be shut down by the control server. Otherwise, later
tasks will receive the ip:ports of invalid evaluation processes. A
simple example to shut down servers is listed here.

.. image:: https://github.com/eyounx/ZOOjl/blob/master/img/control_server.png?raw=true
