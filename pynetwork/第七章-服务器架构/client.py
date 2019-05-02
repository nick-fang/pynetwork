"""代码清单7-2 用于《python之禅》示例协议的客户端程序"""
import argparse
import random
import socket
import zen_utils

def client(address, cause_error=False):
    """用于提问的客户端；cause_error为True时，故意不发送【?】定界符，来检测服务器端的异常处理能力"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    aphorisms = list(zen_utils.aphorisms)
    if cause_error:
        sock.sendall(aphorisms[0][:-1]) #故意发送一个不含【?】定界符的问题
        return #不做任何操作，直接返回
    for aphorism in random.sample(aphorisms, 3): #在一个【连接套接字】上，与服务器端进行3次对话：sendall()+recvall()
        sock.sendall(aphorism) #发送问题
        print(aphorism, zen_utils.recv_until(sock, b'.')) #在一行中打印发送的问题，和收到的答案
    sock.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='example client')
    parser.add_argument('host', help='IP or hostname')
    parser.add_argument('-e', action='store_true', help='cause an error')
    parser.add_argument('-p', metavar='port', type=int, default=1060, help='TCP port (default 1060)')
    args = parser.parse_args()
    address = (args.host, args.p)
    client(address, args.e)
