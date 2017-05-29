from calculator_server import CalculatorServer
from fx import setcover


# asynchronous racos
if True:
    data_length = 1024
    server_ip = '127.0.0.1'
    server_port = 3001

    # set server ip, port and longest data length in initialization
    server = CalculatorServer(server_ip, server_port, data_length)
    # set objective function when starting server
    server.start_server(func=setcover)
