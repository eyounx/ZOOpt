---------------------------------
Quick Start of Distributed ZOOpt
---------------------------------
Distributed ZOOpt is the distributed version of
`ZOOpt <https://github.com/eyounx/ZOOpt>`__. In order to improve the
efficiency of handling distributed computing, we use Julia language to
code the client end for its high efficiency and Python-like features (
`ZOOclient <https://github.com/eyounx/ZOOjl.jl>`__ ). Meanwhile, the
servers are still coded in Python
(`ZOOsrv <https://github.com/eyounx/ZOOsrv>`__) . Therefore, a user can
program the objective function in Python as usual, and only need to
change a few lines of the client Julia codes (just as easy to understand
as Python).

Two zeroth-order optimization methods are implemented in Distributed
ZOOpt release 0.1, respectively are Asynchronous Sequential RACOS
(ASRacos) method and parallel pareto optimization for subset selection
method (PPOSS, IJCAI'16)

Installation
------------

Distributed ZOOpt contains two parts:
`ZOOclient <https://github.com/eyounx/ZOOjl.jl>`__ and
`ZOOsrv <https://github.com/eyounx/ZOOsrv>`__.

Install ZOOclient
~~~~~~~~~~~~~~~~~

The client only needs to be installed in the client node. The client is
written in Julia scripts, if you have not done so already, `download and
install Julia <http://julialang.org/downloads/>`__ (Any version starting
with 0.6 should be fine)

To install ZOOclient, start Julia and run:

.. code:: julia

    Pkg.add("ZOOclient")

This will download ZOOclient support codes and all of its dependencies.

Install ZOOsrv
~~~~~~~~~~~~~~

We have two type of servers, the control server and the evaluation
server. Only one control server is needed in the network, and every
computing node needs to run an evaluation server. The two servers are
both in the ZOOsrv package. The easiest way to get ZOOsrv is to type
``pip install zoosrv`` in you terminal/command line.

If you want to install ZOOsrv by source code, download `this
project <https://github.com/eyounx/ZOOsrv>`__ and sequentially run
following commands in your terminal/command line.

::

    $ python setup.py build
    $ python setup.py install

An Example of Using Distributed ZOOpt in Single Machine
-------------------------------------------------------

In this example, we only have one machine. Thus the client, control
server, and evaluation server are all run in the machine.

Launch Servers
~~~~~~~~~~~~~~

Launch a control server
^^^^^^^^^^^^^^^^^^^^^^^

Write a simple start\_control\_server.py, including the following codes
`(Example code in
ZOOsrv) <https://github.com/eyounx/ZOOsrv/blob/master/example/start_control_server.py>`__

.. code:: python

    from zoosrv import control_server
    control_server.start(20000)

where the parameter 20000 is the listening port of the control server.
Then, run the codes as in command line

::

    python start_control_server.py

Launch an evaluation server
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Write a start\_evaluation\_server.py, including the following codes
`(Example code in
ZOOsrv) <https://github.com/eyounx/ZOOsrv/blob/master/example/start_evaluation_server.py>`__

.. code:: python

    from zoosrv import evaluation_server
    evaluation_server.start("evaluation_server.cfg")

where evaluation\_server.cfg is the configuration file.

Then, write the evaluation\_server.cfg file including the following
lines: `(Example code in
ZOOsrv) <https://github.com/eyounx/ZOOsrv/blob/master/example/evaluation_server.cfg>`__

::

    [evaluation server]
    shared fold = /path/to/project/ZOOsrv/example/objective_function/
    control server ip_port = 127.0.0.1:20000
    evaluation processes = 10
    starting port = 60003
    ending port = 60020

where ``shared fold`` is the fold storing the objective function files.
``control server ip_port`` is the address of the control server, and the
last three lines state we want to start 10 evaluation processes by
choosing 10 available ports from 60003 to 60020.

Finally, launch the evaluation server in command line

::

    python start_evaluation_server.py

Perform Optimization
~~~~~~~~~~~~~~~~~~~~

We try to optimize the Ackley function.

Define the objective function in Python
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Write ``fx.py`` including the following codes `(Example code in
ZOOsrv) <https://github.com/eyounx/ZOOsrv/blob/master/example/objective_function/fx.py>`__

.. code:: python

    import numpy as np
    def ackley(solution):
        x = solution.get_x()
        bias = 0.2
        value = -20 * np.exp(-0.2 * np.sqrt(sum([(i - bias) * (i - bias) for i in x]) / len(x))) - \
                np.exp(sum([np.cos(2.0*np.pi*(i-bias)) for i in x]) / len(x)) + 20.0 + np.e
        return value

where ``shared fold`` is the directory the ``fx.py`` stores.

Write client code in Julia
^^^^^^^^^^^^^^^^^^^^^^^^^^

Write ``client.jl`` including the following codes `(Example code in
ZOOsrv) <https://github.com/eyounx/ZOOjl.jl/blob/master/example/client.jl>`__

.. code:: julia

    using ZOOclient
    using PyPlot

    # define a Dimension object
    dim_size = 100
    dim_regs = [[-1, 1] for i = 1:dim_size]
    dim_tys = [true for i = 1:dim_size]
    mydim = Dimension(dim_size, dim_regs, dim_tys)
    # define an Objective object
    obj = Objective(mydim)

    # define a Parameter Object, the five parameters are indispensable.
    # budget:  number of calls to the objective function
    # evalueation_server_num: number of evaluation cores user requires
    # control_server_ip_port: the ip:port of the control server
    # objective_file: objective funtion is defined in this file
    # func: name of the objective function
    par = Parameter(budget=10000, evaluation_server_num=10, control_server_ip_port="127.0.0.1:20000",
        objective_file="fx.py", func="ackley")

    # perform optimization
    sol = zoo_min(obj, par)
    # print the Solution object
    sol_print(sol)

    # visualize the optimization progress
    history = get_history_bestsofar(obj)
    plt[:plot](history)
    plt[:savefig]("figure.png")

Now, we can run the client file to perform the optimization

::

    $ ./julia -p 4 /absolute/path/to/your/file/client.jl

where ``julia -p n`` provides ``n`` processes for the client on the
local machine. Generally it makes sense for ``n`` to equal the number of
CPU cores on the machine.

For a few seconds, the optimization is done and we will get the result.

.. image:: https://github.com/eyounx/ZOOjl.jl/blob/master/img/result.png?raw=true

Visualized optimization progress looks like:

.. image:: https://github.com/eyounx/ZOOjl.jl/blob/master/img/figure.png?raw=true

| ​
| ​
| ​
