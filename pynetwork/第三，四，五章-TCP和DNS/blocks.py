"""代码清单5-2 封帧模式五：使用长度前缀将每个数据块封装成帧"""
import socket
import struct
import argparse

header_struct = struct.Struct('!I') #该对象预编译了一个4字节无符号整型的模板/pattern
def recvall(sock, length):
    """自定义的接收函数，能够确保接收到length长度的TCP数据包"""
    data_received = b''
    while length:
        block = sock.recv(length)
        if not block:
            raise EOFError('socket closed with {} bytes left in this block'.format(length))
        length -= len(block) #每次循环，都从消息总长度中扣除掉接收到的长度，直到总长度被削减为零
        data_received += block
    return data_received

def get_block(sock):
    """接收一个TCP帧：先使用struct模块解包长度前缀，再接收相应长度的数据包（即消息本体字节串）"""
    data = recvall(sock, header_struct.size) #先接收消息的前4个字节；header_struct.size代表该pattern匹配对象占用的字节数
    (block_length,) = header_struct.unpack(data) #将这前4个字节解包，获得消息长度，是个int
    return recvall(sock, block_length) #再接收消息本体的字节串

def put_block(sock, message):
    """TCP封帧：先发送经过struct模块打包的长度前缀，再发送消息本体字节串"""
    block_length = len(message)
    sock.send(header_struct.pack(block_length)) #使用struct模块打包数据块的长度，是为了保证代表长度的整数始终占用【定长】的字节数
    sock.send(message) #先发送消息的长度的字节串，再发送消息本体的字节串；因为接收端知道消息长度，它会阻塞直到接收到整个数据块，所以发送端可以不使用sendall()方法

def server(address):
    """服务器端"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(1)
    print('run this script in another window with "-c" to connect')
    print('listening at', sock.getsockname())
    sc, sockname = sock.accept() #创建连接套接字
    print('accepted connection from', sockname)
    sc.shutdown(socket.SHUT_WR) #设置单向套接字；服务器端不再向外发送数据包
    while True: #接收一次就解析一次，而不是接收完毕后再一次性解析
        block = get_block(sc) #接收并解析客户端发送的字节串
        if not block:
            break
        print('block says:', repr(block)) #打印解析结果
    sc.close()
    sock.close()

def client(address):
    """客户端"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address) #创建连接套接字
    sock.shutdown(socket.SHUT_RD) #设置单向套接字；客户端不再接收外面传来的数据包
    put_block(sock, b'beautiful is better than ugly.')
    put_block(sock, b'explicit is better than implicit.')
    put_block(sock, b'simple is better than complex.')
    put_block(sock, b'')
    sock.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='transmit & receive blocks over TCP')
    parser.add_argument('hostname', nargs='?', default='127.0.0.1', help='IP address or hostname (default 127.0.0.1)')
    parser.add_argument('-c', action='store_true', help='run as the client')
    parser.add_argument('-p', type=int, metavar='port', default=1060, help='TCP port number (default 1060)')
    args = parser.parse_args()
    function = client if args.c else server
    function((args.hostname, args.p))
