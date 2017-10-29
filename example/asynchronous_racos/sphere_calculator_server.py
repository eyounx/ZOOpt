import sys
sys.path.append("/Users/liu/Desktop/CS/github/ZOO/")

import multiprocessing
from zoopt.algos.asynchronous_racos import calculator_server
from sys import argv


# test function
def run_server(ip, port):
    data_length = 1024
    server_ip = ip
    server_port = port

    # set server ip, port and longest data length in initialization
    server = calculator_server.CalculatorServer(server_ip, server_port, data_length)

    server.start_server(control_server="127.0.0.1:20000", working_dir="/Users/liu/Desktop/CS/github/ZOO/example/"
                                                                      "asynchronous_racos/sphere.py", func='sphere')

if __name__ == "__main__":
    file_obj = open("configuration.txt")
    list_of_all_lines = file_obj.readlines()
    ips = []
    ports = []
    for line in list_of_all_lines:
        result = line.split()
        ips.append(result[0])
        ports.append(result[1])
    workers = []
    for i in range(len(ips)):
        ip = ips[i]
        port = int(ports[i])
        workers.append(multiprocessing.Process(target=run_server, args=(ip, port,)))
    for w in workers:
        w.start()
