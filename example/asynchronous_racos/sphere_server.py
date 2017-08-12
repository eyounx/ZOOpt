from zoopt.algos.asynchronous_racos.calculator_server import CalculatorServer


# Sphere function for continue optimization
def sphere(solution):
    x = solution.get_x()
    value = sum([(i-0.2)*(i-0.2) for i in x])
    return value


# test function
def run_server():
    data_length = 2048
    server_ip = '127.0.0.1'
    server_port = 9999

    # set server ip, port and longest data length in initialization
    server = CalculatorServer(server_ip, server_port, data_length)

    server.start_server(func=sphere)

if __name__ == "__main__":
    run_server()