from calculator_server import  CalculatorServer
from fx import sphere, ackley, setcover, mixed_function
import socket
# asynchronous racos
if True:
    data_length = 1024
    server_ip = '127.0.0.1'
    server_port = 3001

    obj = socket.socket()
    obj.connect((server_ip, server_port))
    x = [0.2, 0.1, 0.1, 0.3]
    obj.sendall(bytes(x))
    while True:
        ret_bytes = obj.recv(data_length)
        ret_str = str(ret_bytes)
        print ret_str

