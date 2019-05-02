"""代码清单2-4 UDP广播"""
import argparse
import socket

BUFSIZE = 65535

def server(interface, port):
    """服务器端"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface, port))
    print('listening for datagrams at {}'.format(sock.getsockname()))
    while True:
        data, address = sock.recvfrom(BUFSIZE)
        text = data.decode('ascii')
        print('the client at {} says: {!r}'.format(address, text))

def client(network, port):
    """客户端，广播的发布者；network参数代表整个内网，也就是【广播地址】"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) #将该UDP套接字设置为允许广播
    text = 'broadcast datagram!'
    sock.sendto(text.encode('ascii'), (network, port))

if __name__ == "__main__":
    choices = {'client':client, 'server':server}
    parser = argparse.ArgumentParser(description='send, receive UDP broadcast')
    parser.add_argument('role', choices=choices, help='which role to take')
    parser.add_argument('host', help='interface the server listens at; network the client sends to')
    parser.add_argument('-p', metavar='port', type=int, default=1060, help='UDP port (default 1060)')
    args = parser.parse_args()
    fuction = choices[args.role]
    fuction(args.host, args.p)
