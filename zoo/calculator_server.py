import socket
from zoo.utils.tool_function import ToolFunction


class CalculatorServer:

    def __init__(self, s_ip, s_port, data_len):

        self.__server_ip = s_ip                     # server ip
        self.__server_port = s_port                 # server port
        self.__data_length = data_len               # data length
        return

    def start_server(self, objective=None):

        # define objective function
        calculate = objective

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #
        s.bind((self.__server_ip, self.__server_port))
        s.listen(5)

        all_connect = 0
        pro_list = []

        s_ip = ''
        s_port = 0

        # print 'this is SetCover server 1!'
        print 'waiting for connector...'

        while True:

            # get x from client
            cs, address = s.accept()
            # print all_connect + 1, ' get connected...'
            all_connect += 1
            print 'connect num:', all_connect, ' address:', address
            cs.send('connected')
            mess = cs.recv(1024)
            if mess == 'exit':
                break
            s_ip, s_port = self.explain_address(mess)
            cs.send('received address')
            mess = cs.recv(1024)
            if mess != 'next is data':
                continue
            cs.send('ready')
            data_str = cs.recv(self.__data_length)
            cs.send('received')
            cs.close()

            # calculate fx
            x = []
            data_str = data_str.split(' ')
            for i in range(len(data_str)):
                x.append(float(data_str[i]))
            fx = calculate(x=x)
            fx_x = self.result_2_string(fx=fx, x=x)

            # send result back
            fx_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                fx_server.connect((s_ip, s_port))
            except socket.error, e:
                print 'connect error %s' % e
                continue
            try:
                mess = fx_server.recv(1024)
            except socket.error, e:
                print 'receive error %s' % e
                continue
            if mess != 'connected':
                fx_server.close()
                continue
            fx_server.send(self.__server_ip + ':' + str(self.__server_port))
            mess = fx_server.recv(1024)
            if mess != 'received address':
                fx_server.close()
                continue
            fx_server.send('ready for fx')
            mess = fx_server.recv(1024)
            if mess != 'ready':
                fx_server.close()
                continue
            fx_server.send(fx_x)
            mess = fx_server.recv(1024)
            if mess == 'received':
                print 'pass result finished! ', fx_x
            print 'send result finished...'
            fx_server.close()
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

