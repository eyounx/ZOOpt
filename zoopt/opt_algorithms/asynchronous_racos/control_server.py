"""
This module contains the class ControlServer.

Author:
    Yu-Ren Liu
"""

import threading
import socket
from receive import receive
from zoopt.utils.tool_function import ToolFunction
import copy


class ControlServer:
    """
    Control server is responsible for managing all evaluation servers.
    """
    def __init__(self, ip, port):
        """
        Initialization.

        :param ip: ip address of the control server, e.g., "127.0.0.1"
        :param port:
            ports occupied by the control server, it's a list having four elements, e.g., [10000, 10001, 10002, 10003]
            respectively are occupied by function receive_from_evaluation_server, send_to_client and receive_from_client, restart_evaluation_server
        """
        self.ip = ip
        self.port = port
        # for example, elements are ["192.168.1.101:5555", "192.168.1.102:10000"]
        self.evaluation_server = []

    def receive_from_evaluation_server(self, lock):
        """
        Receive ip_port from evaluation server
        :param lock: lock on self.evaluation_server
        :return: no return
        """

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #
        s.bind((self.ip, self.port[0]))
        s.listen(5)
        while True:
            es, address = s.accept()
            ip_port = es.recv(1024)
            with lock:
                if ip_port not in self.evaluation_server:
                    self.evaluation_server.append(ip_port)
                    ToolFunction.log("receive ip_port from evaluation server: " + ip_port)

    def send_to_client(self, lock):
        """
        Send evaluation_server ip:port to client.

        :param lock: lock on self.evaluation_server
        :return: no return
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #
        s.bind((self.ip, self.port[1]))
        s.listen(5)
        while True:
            client, address = s.accept()
            require_num = int(client.recv(1024))
            require_num = min(require_num, len(self.evaluation_server))
            msg = ""
            with lock:
                for i in range(require_num):
                    if i == 0:
                        msg += self.evaluation_server[i]
                    else:
                        msg = msg + ' ' + self.evaluation_server[i]
                msg += '\n'
                print(msg)
                self.evaluation_server = self.evaluation_server[require_num:]
                client.sendall('get %d evaluation server\n' % require_num)
                client.sendall(msg)

    #
    def receive_from_client(self, lock):
        """
        Receive evaluation server ip_ports from client.

        :param lock: lock on self.evaluation_server
        :return: no return
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #
        s.bind((self.ip, self.port[2]))
        s.listen(5)
        # print("in receive from client")
        while True:
            client, address = s.accept()
            data_str = receive(1024, client)
            ToolFunction.log("receive ip_port from client: " + data_str)
            ip_ports = data_str.split()
            with lock:
                for ip_port in ip_ports:
                    if ip_port not in self.evaluation_server:
                        self.evaluation_server.append(ip_port)

    def restart_evaluation_server(self, lock):
        """
        Restart evaluation servers based on ip:ports received from client.

        :param lock: lock on self.evaluation_server
        :return: no return
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #
        s.bind((self.ip, self.port[3]))
        s.listen(5)
        # print("in receive from client")
        while True:
            client, address = s.accept()
            data_str = receive(1024, client)
            ToolFunction.log("client exception, receive ip_port from client: " + data_str)
            ip_ports = data_str.split()
            with lock:
                for ip_port in ip_ports:
                    if ip_port not in self.evaluation_server:
                        ip, port = ip_port.split(":")
                        port = int(port)
                        addr = (ip, port)
                        s.connect(addr)
                        s.sendall("control server: restart\n")
                        self.evaluation_server.append(ip_port)

    def start(self):
        """
        Start this control server.
        :return: no return
        """
        lock = threading.RLock()
        # start threads
        worker = []
        worker.append(threading.Thread(target=self.receive_from_evaluation_server, args=(lock,)))
        worker.append(threading.Thread(target=self.send_to_client, args=(lock,)))
        worker.append(threading.Thread(target=self.receive_from_client, args=(lock,)))
        worker.append(threading.Thread(target=self.restart_evaluation_server, args=(lock,)))
        for t in worker:
            t.setDaemon(True)
            t.start()
        # start main thread
        while True:
            cmd = int(raw_input("please input cmd, 1: print servers, 2: shut down the server\n"))
            with lock:
                if cmd == 1:
                    ToolFunction.log(str(self.evaluation_server))
                elif cmd == 2:
                    self.shut_down_control()

    def shut_down_control(self):
        """
        Shut down evaluation servers.

        :return: no return
        """
        try:
            print("you can input three different kinds of commands")
            print("1.all ==> shut down all servers. e.g. all")
            print("2.ip:ip1 ==> shut down all servers having ip1 as ip. e.g. ip:127.0.0.1")
            print("3.ip_port: ip1:port1 ip2:port2 ip3:port3 ... ==> shut down specific servers. e.g. ip_port: 127.0.0.1:20000 127.0.0.1:20001")
            msg = raw_input("")
            print(msg)
            new_cal_server = copy.deepcopy(self.evaluation_server)
            if msg == "all":
                print("in all")
                for ip_port in self.evaluation_server:
                    self.shut_down(ip_port)
                    new_cal_server.remove(ip_port)
            elif msg[:7] == "ip_port":
                print("in ip_port")
                ip_ports = msg[9:].split(' ')
                for ip_port in ip_ports:
                    self.shut_down(ip_port)
                    new_cal_server.remove(ip_port)
            elif msg[:2] == "ip":
                print("in ip")
                ip = msg[3:]
                for ip_port in self.evaluation_server:
                    sip, port = ip_port.split(":")
                    if sip == ip:
                        self.shut_down(ip_port)
                        new_cal_server.remove(ip_port)
            else:
                print("No such command")
            self.evaluation_server = new_cal_server
        except Exception as e:
            print("input error", e)

    def shut_down(self, ip_port):
        """
        Shut down one evaluation server, which bounds to ip_port.

        :param ip_port: ip:port of the evaluation server
        :return: no return
        """
        es = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #
        if ip_port not in self.evaluation_server:
            ToolFunction.log("no such ip:port")
            return
        print(ip_port)
        ip, port = ip_port.split(":")
        port = int(port)
        addr = (ip, port)
        es.connect(addr)
        es.sendall("control server: shutdown#")
        result = receive(1024, es)
        print(result)
        if result == "success":
            ToolFunction.log("manage to shut down")
        else:
            ToolFunction.log("fail to shut down")
        es.close()
