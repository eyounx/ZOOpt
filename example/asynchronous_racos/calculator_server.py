import sys
sys.path.append("/Users/liu/Desktop/CS/github/ZOO/")

import socket
import multiprocessing
from zoopt.algos.asynchronous_racos import calculator_server
from port_conflict import is_open
from zoopt.utils.tool_function import ToolFunction


def run_server(port, work_dir, control_server):
    local_ip = socket.gethostbyname(socket.gethostname())
    data_length = 1024
    server_ip = local_ip
    server_port = port

    # set server ip, port and longest data length in initialization
    server = calculator_server.CalculatorServer(server_ip, server_port, data_length)

    server.start_server(control_server=control_server, working_dir=work_dir)


# configuration is a file name
# configuration  has three lines
# the first line is the working directory this server works on
# the second line is the address of control server
# the third line has three numbers, for example, 2 50000 50002
# 2 means opening 2 server, 50000 50002 means these servers can use port between 50000 and 50002([50000, 50002])
def run(configuration):
    file_obj = open(configuration)
    list_of_all_lines = file_obj.readlines()
    working_dir = list_of_all_lines[0][:-1]
    control_server = list_of_all_lines[1][:-1]
    info = list_of_all_lines[2].split()
    num = int(info[0])
    lowerb = int(info[1])
    upperb = int(info[2])
    local_ip = socket.gethostbyname(socket.gethostname())  # get local ip
    ToolFunction.log("calculator server ip: " + local_ip)
    count = 0
    workers = []
    for port in range(lowerb, upperb):
        if is_open(local_ip, port) is False:
            count += 1
            workers.append(multiprocessing.Process(target=run_server, args=(port, working_dir, control_server)))
            if count >= num:
                break
    for w in workers:
        w.start()

if __name__ == "__main__":
    run("configuration.txt")
