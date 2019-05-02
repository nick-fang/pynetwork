"""代码清单3-1 封帧模式三：定长数据包；简单的TCP服务器和客户端"""
import argparse
import socket

def recvall(sock, length):
    """自定义的recvall函数，接收指定长度的数据包"""
    data_received = b''
    while len(data_received) < length: #设置循环，保证length长度的数据全部被接收
        chunk = sock.recv(length - len(data_received)) #TCP的recv(buffsize)函数，只能尝试接收buffsize个字节的数据，但是无法保证这些数据能够一次全部接收
        if not chunk: #如果客户端关闭了【连接套接字】，16个字节的数据却还没有全部接收到
            raise EOFError('was expecting {} bytes but only received {} bytes before the socket closed'.format(length, len(data_received)))
        data_received += chunk
    return data_received

def server(interface, port):
    """服务器端"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #使用TCP协议
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #设置sock对象的选项
    sock.bind((interface, port)) #将服务器程序显式绑定到要监听的端口上
    sock.listen(1) #将该sock声明为监听套接字,并且同一时刻只允许一个客户端请求被压栈等待，更多的连接请求会被直接忽略
    print('listening at', sock.getsockname())
    while True: #监听死循环
        print('waiting to accept a new connection')
        conn, sockname = sock.accept() #监听套接字接收客户端发来的连接请求，并返回一个新的连接套接字，用来管理两主机间的这次网络会话；如果没有接收到客户端的连接请求，则死循环会阻塞在这一步
        print('we have accepted a connection from', sockname)
        print('\tsocket name:', conn.getsockname())
        print('\tsocket peer:', conn.getpeername())
        message = recvall(conn, 16) #接收客户端发来的数据包的前16个字节
        print('\tincoming sixteen-octet messsage:', repr(message))
        conn.sendall(b'farewell, client') #向客户端发送16个字节的数据包
        conn.close()
        print('\treply sent, socket closed')

def client(host, port):
    """客户端"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port)) #将该sock声明为连接套接字，并且主动向服务器端发起连接请求（不同于UDP的connect函数？？）
    print('client has been assigned socket name', sock.getsockname())
    sock.sendall(b'hi there, server') #向服务器端发送16个字节的数据包
    reply = recvall(sock, 16) #接收服务器端发来的数据包的前16个字节
    print('the server said', repr(reply))
    sock.close()

if __name__ == "__main__":
    CHOICES = {'client':client, 'server':server}
    parser = argparse.ArgumentParser(description='send and receive over TCP')
    parser.add_argument('role', choices=CHOICES, help='which role to play') #choices参数使用字典的情况下，程序只会拿该字典的键与命令行参数做匹配
    parser.add_argument('host', help='interface the server listens at; host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='TCP port (default 1060)')
    args = parser.parse_args()
    function = CHOICES[args.role] #解析出的args是个具名元组，args.role就是命令行中输入的选项
    function(args.host, args.p)
