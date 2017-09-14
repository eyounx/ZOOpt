import sys
sys.path.append("/home/lamda/liuyr/ZOO/")

from zoopt.algos.asynchronous_racos import calculator_server
from sys import argv
from random import Random
# Sphere function for continue optimization

def sphere(solution):
    a = 0
    rd = Random()
    for i in range(1000000):
        a += rd.uniform(0, 1)
    x = solution.get_x()
    value = sum([(i-0.2)*(i-0.2) for i in x])
    return value


# test function
def run_server(ip, port):
    data_length = 1024
    server_ip = ip
    server_port = port

    # set server ip, port and longest data length in initialization
    server = calculator_server.CalculatorServer(server_ip, server_port, data_length)

    server.start_server(func=sphere)

if __name__ == "__main__":
    ip = argv[1]
    port = int(argv[2])
    run_server(ip, port)
