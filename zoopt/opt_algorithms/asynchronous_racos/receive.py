"""
This module contains the function 'receive', which receives data from evaluation server.

Author:
    Yu-Ren Liu
"""


def receive(data_length, es):
    """
    Receive data from evaluation server and remove useless characters.

    :param data_length: length of the data received
    :param es: evaluation server
    :return: data received
    """
    data_str = ""
    while True:
        data_tmp = es.recv(data_length)
        stop = data_tmp.find("#")
        if stop > 0:
            data_tmp = data_tmp[0:stop]
            data_str += data_tmp
            break
        else:
            data_str += data_tmp
    if data_str[0] == '\n':
        data_str = data_str[1:]
    if data_str[-1] == '\n':
        data_str = data_str[:-1]
    return data_str
