import sys
sys.path.append("/Users/liu/Desktop/CS/github/ZOO/")

from zoopt.algos.asynchronous_racos.control_server import ControlServer

if __name__ == "__main__":
    cs = ControlServer("127.0.0.1", [20000, 20001, 20002])
    cs.start()
