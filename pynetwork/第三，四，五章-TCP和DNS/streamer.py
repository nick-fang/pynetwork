"""代码清单5-1 封帧模式一：单向套接字；直接发送所有数据，然后关闭连接"""
import socket
import argparse

def server(address):
    """服务器端"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(1)
    print('run this script in another window with "-c" to connect')
    print('listen at', sock.getsockname())
    conn, sockname = sock.accept() #创建连接套接字，连接客户端
    print('accepted connection from', sockname)
    conn.shutdown(socket.SHUT_WR) #设置单向套接字；服务器端不再向外发送数据包
    message = b''
    while True:
        data = conn.recv(8192)
        if not data: #如果客户端关闭套接字，则服务器端会收到空字节串，于是跳出循环
            print('received zero bytes - end of file')
            break
        print('received {} bytes'.format(len(data)))
        message += data #用message变量，接收客户端发送的所有数据包，并拼接成完整的字节串
    print('message:\n')
    print(message.decode('ascii')) #等到客户端发送完毕并关闭套接字后，才开始解析/处理收到的字节串
    conn.close()
    sock.close()

def client(address):
    """客户端"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address) #创建连接套接字，连接服务器端
    sock.shutdown(socket.SHUT_RD) #设置单向套接字；客户端不再接受外面传来的数据包
    sock.sendall(b'beautiful is better than ugly.\n')
    sock.sendall(b'explicit is better than implicit.\n')
    sock.sendall(b'simple is better than complex.\n')
    sock.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='transmit & receive a data stream')
    parser.add_argument('hostname', nargs='?', default='127.0.0.1', help='IP address or hostname(default 127.0.0.1)')
    parser.add_argument('-c', action='store_true', help='run as client')
    parser.add_argument('-p', type=int, metavar='port', default=1060, help='TCP port number (default 1060)')
    args = parser.parse_args()
    function = client if args.c else server
    function((args.hostname, args.p))
