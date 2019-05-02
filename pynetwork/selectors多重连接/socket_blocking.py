"""使用上下文管理器构建TCP套接字：echo-server"""
import socket
import argparse

def server(host, port):
    """服务器端"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: #程序结束后自动关闭该【监听套接字】
        sock.bind((host, port)) #绑定到一个地址+端口上
        sock.listen() #将该套接字声明为【监听套接字】
        print('listening at:', sock.getsockname())
        while True: #监听死循环，保证服务器端持续监听下去
            conn, addr = sock.accept() #监听套接字接收客户端发来的连接请求，并返回一个新的连接套接字
            with conn: #会话结束后自动关闭该【连接套接字】
                print('connected by', addr)
                while True: #recvall循环，保证客户端的一次send能够全部被接收
                    data = conn.recv(1024) #“尝试”接收1024字节
                    if not data: #如果data是个空字节串，说明客户端在发送完数据后，关闭了其连接套接字的发送方向
                        break #跳出循环，因此会自动关闭连接套接字 - conn
                    conn.sendall(data) #将接收到的data全部发送回客户端
                    print('echoing', repr(data), 'to', addr)

def client(host, port):
    """客户端"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port)) #向该地址的服务器端发出连接请求
        sock.sendall(b'simple is better than complex.') #发送一条消息
        sock.shutdown(socket.SHUT_WR) #发送消息后，主动关闭套接字的send方向，使得服务器端能够跳出recvall循环
        while True: #recvall循环，保证服务器端返回的数据能够全部被接收到
            data = sock.recv(1024) #“尝试”接收1024字节
            print('received:', data)
            if not data: #如果data是个空字节串，说明服务器端关闭了连接套接字
                print('server socket closed.')
                break #跳出循环，因此会自动关闭连接套接字 - sock

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='an echo-server using context manager')
    parser.add_argument('-n', metavar='hostname', default='127.0.0.1')
    parser.add_argument('-p', metavar='port', type=int, default=65432)
    parser.add_argument('-c', action='store_true', help='run as the client')
    args = parser.parse_args()
    run = client if args.c else server #如果命令行中没有指定'-c'参数，则args.c属性值默认为None
    run(args.n, args.p)
