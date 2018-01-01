"""
This file contains the class CalculatorServer.

Author:
    Yu-Ren Liu
"""

import socket
from zoopt.solution import Solution
from loader import Loader
from receive import receive


class EvaluationServer:
    """
        Evaluation server ,an important part in asynchronous racos, is responsible for
        evaluating solution sent by client.
    """
    def __init__(self, s_ip, s_port, data_len):
        """
        Initialization.

        :param s_ip: server ip
        :param s_port: server port
        :param data_len: data length in tcp
        """
        self.__server_ip = s_ip
        self.__server_port = s_port
        self.__data_length = data_len

        return

    def start_server(self, control_server, working_dir):
        """
        Start this evaluation server.

        :param control_server: control server address
        :param working_dir: current working directory
        :return: target function name
        """

        # send evaluation server address to control server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.explain_address(control_server)))
        s.sendall(self.__server_ip + ':' + str(self.__server_port))
        s.close()

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.__server_ip, self.__server_port))
        s.listen(5)
        all_connect = 0
        restart = False
        print("this is server !")
        print ("waiting for connector...")
        while True:
            # get x from client
            es, address = s.accept()
            # print all_connect + 1, ' get connected...'
            all_connect += 1
            print("connect num:"+str(all_connect)+" address:"+str(address))
            cmd = receive(self.__data_length, es)
            if cmd == "control server: shutdown":
                es.sendall("success#")
                break
            elif cmd == "client: calculate":
                try:
                    es.sendall("calculate\n")
                    msg = receive(self.__data_length, es)
                    addr, func = msg.split(":")
                    es.sendall("receive\n")

                    load = Loader()
                    module = load.load(working_dir + addr)
                    calculate = module[func]
                    data = receive(self.__data_length, es)
                    x = []
                    data_str = data.split(' ')
                    # print(data_str)
                    for istr in data_str:
                        x.append(float(istr))
                    fx = calculate(Solution(x=x))
                    fx_x = str(fx) + "\n"
                    es.sendall(fx_x)
                    print("finish calculating")
                except Exception, msg:
                    print("Exception")
                    es.sendall("Exception: " + str(msg))
                    restart = True
                    break
                # print ("send result finished, result: " + str(fx_x))
            elif cmd == "control server: restart":
                restart = True
                break
            else:
                print(cmd)
                print("no such cmd")
            es.close()
        print ("server close!")
        s.close()
        if restart is True:
            print("server restart")
            self.start_server(control_server, working_dir)

    def result_2_string(self, fx=0, x=[0]):
        """
        Transfer result value to string, which has the form "fx: x"
        :param fx:
        :param x:
        :return:
        """
        my_string = str(fx) + ':' + self.list2string(x)
        return my_string

    def list2string(self, list):
        """
        Transfer a list to string, [x1, x2, x3] --> 'x1 x2 x3'.
        :param list: input list
        :return: a string
        """
        my_str = str(list[0])
        i = 1
        while i < len(list):
            my_str = my_str + ' ' + str(list[i])
            i += 1
        return my_str

    def explain_address(self, addr):
        """
        Get ip and port from ad`dress 'ip:port'. Ip is a string and port is a integer.

        :param addr: address
        :return: ip and port
        """
        addr = addr.split(':')
        t_ip = addr[0]
        t_port = int(addr[1])
        return t_ip, t_port

