"""
This file contains a function judging whether a port is occupied.

Author:
    Yu-Ren Liu
"""

import socket


def is_open(ip, port):
    """
    Judge whether a port is occupied or not.

    :param ip: ip address
    :param port: port number
    :return: True or False
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((ip, port))
    if result == 0:
        print("Port %d is already in use")
        return True
    else:
        return False

