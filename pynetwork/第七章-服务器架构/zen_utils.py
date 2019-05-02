"""代码清单7-1 封帧模式四：定界符；支持《python之禅》示例协议的数据与规则"""
import argparse
import socket
import time

aphorisms = {b'beautiful is better than?':b'ugly.',
             b'explicit is better than?':b'implicit.',
             b'simple is better than?':b'complex.'}

def get_answer(aphorism):
    """返回针对《python之禅》的问题的答案"""
    time.sleep(0.0) #模拟网络延时？？
    return aphorisms.get(aphorism, b'Error: unknown aphorism.') #从字典中取值

def parse_command_line(description):
    """提取并解析命令行参数中的IP地址和端口号"""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('host', help='IP or hostname')
    parser.add_argument('-p', metavar='port', type=int, default=1060, help='TCP port (default 1060)')
    args = parser.parse_args()
    address = (args.host, args.p)
    return address

def create_srv_socket(address):
    """创建一个服务器的【监听套接字】，服务器通过后者来接收连接请求"""
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(address)
    listener.listen(64) #同时接收64个客户端？？
    print('listening at {}'.format(listener.getsockname()))
    return listener

def accept_connections_forever(listener):
    """在给定的【监听套接字】上，持续监听并接受客户端的连接请求，并据此创建【连接套接字】"""
    while True: #监听死循环
        sock, address = listener.accept()
        print('accepted connection from {}'.format(address))
        handle_conversation(sock, address)

def handle_conversation(sock, address):
    """与客户端保持对话，直到客户端主动关闭【连接套接字】"""
    try:
        while True: #保证在一个【连接套接字】上，持续接收客户端的多次sendall()；相当于【循环recvall()】
            handle_request(sock) #一次recvall()
    except EOFError as exc: #客户端关闭了【连接套接字】，分2种情况
        print('client {} has closed, status: {}'.format(address, exc))
    except Exception as exc: #recvall()中抛出了其他异常
        print('client {} error: {}'.format(address, exc))
    finally:
        sock.close()

def handle_request(sock):
    """与客户端的单次对话：接收问题，发送答案，即一次【recvall()+sendall()】"""
    aphorism = recv_until(sock, b'?') #接收客户端传来的数据包，其结尾应该是一个【?】
    answer = get_answer(aphorism)
    sock.sendall(answer) #将答案完整地发送给客户端，其结尾是一个【.】

def recv_until(sock, suffix):
    """接收客户端发来的字节串，并识别定界符————【?】或【.】；相当于一次recvall()"""
    message = sock.recv(4096) #尝试接收最多4096字节的数据包
    if not message: #如果客户端关闭了【连接套接字】
        raise EOFError('socket closed') #该异常作为一个信号，传递给外层函数，同时可以跳出外层函数的while循环
    while not message.endswith(suffix): #如果message变量的结尾不是【?】，说明客户端发送的这个数据包还未全部接收
        data = sock.recv(4096) #尝试继续接收数据包
        if not data: #如果客户端关闭了【连接套接字】，却直到最后都未发送定界符【?】
            raise EOFError('received {!r} then socket closed'.format(message)) #向外层函数发送另一个信号，同时可以跳出本层函数和外层函数的while循环
        message += data #拼接数据包
    return message
