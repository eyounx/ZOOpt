import sys
sys.path.append("/Users/liu/Desktop/CS/github/ZOO/")

import socket
from zoopt.algos.asynchronous_racos.control_server import ControlServer


# port is a list having four elements, for example, [10000, 10001, 10002, 10003]
def run(port):
    local_ip = socket.gethostbyname(socket.gethostname())
    cs = ControlServer(local_ip, port)
    cs.start()

if __name__ == "__main__":
    run([20000, 20001, 20002, 20003])
