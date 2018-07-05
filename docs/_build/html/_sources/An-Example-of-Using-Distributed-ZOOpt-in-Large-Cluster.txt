-------------------------------------------------------
An Example of Using Distributed ZOOpt in Large Cluster
-------------------------------------------------------

From the previous example, we see how to make ZOOpt use multiple
machines. When having a large cluster of many machines, say a thousand,
it is infeasible to set up every machine manually. The scripts provided
can help set up many machines easier. Specific steps are listed as follows.

1. Set up SSH login without password.
  To use scripts we provided, you should set up SSH login without password on multiple machines. The method can be found 
  `here <https://stackoverflow.com/questions/4388385/how-to-ssh-login-without-password/16604890#16604890>`__.

2. Download dependencies to make sure your machines can run bash and expect scripts.

3. Download `this repository <https://github.com/eyounx/ZOOsrv>`__ and modify variables in ``login_and_deploy.sh``, ``deploy_servers.sh``, ``deploy_servers.exp`` and ``evaluation_server.cfg``.
  The scripts are located in ``ZOOsrv/example`` directory. ``login_and_deploy.sh`` is a script to automatically log in servers. It will 
  then call ``deploy_servers.sh`` to start evaluation servers on different nodes. ``deploy_servers.sh`` will call  ``deploy_servers.exp``
  many times. ``deploy_servers.exp`` is an interactive script to log in one node and start evaluation servers on this node. 

4. Transer this repository to your machines.

5. Start the control server by running ``start_control_server.py`` remotely.

6. Run ``login_and_deploy.sh`` locally to start all evaluation servers.

Detailed codes and their explanation can be found `here <https://github.com/eyounx/ZOOsrv/tree/master/example>`__.