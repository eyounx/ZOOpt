import socket


# def is_open(ip, port):
#     print(ip, port)
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     try:
#         s.connect((ip, port))
#         s.shutdown(2)
#         print('%d is open' % port)
#         return True
#     except Exception, e:
#         print('%d is down' % port)
#         print(e)
#         return False

def is_open(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((ip, port))
    if result == 0:
        print("Port %d is already in use")
        return True
    else:
        return False

