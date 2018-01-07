"""
This file contains example of running control server.

Author:
    Yu-Ren Liu
"""

import sys
sys.path.append("/Users/liu/Desktop/CS/github/ZOO/")

import socket
from zoopt.algos.opt_algorithms.asynchronous_racos import ControlServer
from zoopt.utils.tool_function import ToolFunction

def run(port):
    """
    Api of running control server.

    :param port:
        port of control server
        port is a list having four elements, for example, [10000, 10001, 10002, 10003]
    :return: no return
    """
    local_ip = socket.gethostbyname(socket.gethostname())
    ToolFunction.log("control server ip: " + local_ip)
    cs = ControlServer(local_ip, port)
    cs.start()

if __name__ == "__main__":
    run([20000, 20001, 20002, 20003])
