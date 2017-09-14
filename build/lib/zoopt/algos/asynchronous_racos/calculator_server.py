import socket
from zoopt.solution import Solution


class CalculatorServer:

    def __init__(self, s_ip, s_port, data_len):

        self.__server_ip = s_ip                     # server ip
        self.__server_port = s_port                 # server port
        self.__data_length = data_len               # data length

        return

    def start_server(self, func=None):

        # define objective function
        calculate = func

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #
        s.bind((self.__server_ip, self.__server_port))
        s.listen(5)

        all_connect = 0

        print 'this is server !'
        print 'waiting for connector...'

        while True:
            # get x from client
            cs, address = s.accept()
            # print all_connect + 1, ' get connected...'
            all_connect += 1
            print 'connect num:', all_connect, ' address:', address
            data_str = cs.recv(self.__data_length)
            print(data_str)
            x = []
            data_str = data_str.split(' ')
            print(data_str)
            for i in range(len(data_str)):
                x.append(float(data_str[i]))
            fx = calculate(Solution(x=x))
            fx_x = str(fx)
            cs.send(fx_x)
            print 'send result finished...'
            cs.close()
        print 'server close!'
        s.close()

    def result_2_string(self, fx=0, x=[0]):
        my_string = str(fx) + ':' + self.list2string(x)
        return my_string

    def list2string(self, list):
        my_str = str(list[0])
        i = 1
        while i < len(list):
            my_str = my_str + ' ' + str(list[i])
            i += 1
        return my_str

    def explain_address(self, addr):
        addr = addr.split(':')
        t_ip = addr[0]
        t_port = int(addr[1])
        return t_ip, t_port

