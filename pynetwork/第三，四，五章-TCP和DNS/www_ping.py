"""使用getaddrinfo()创建并连接套接字"""
import argparse
import socket
import sys

def connect_to(hostname_or_ip):
    """Ping一个域名/地址的80端口；先从DNS服务器获取该域名的IP地址，然后创建套接字，尝试连接该IP地址"""
    try:
        infolist = socket.getaddrinfo(hostname_or_ip, 'www', 0, socket.SOCK_STREAM, 0, socket.AI_ADDRCONFIG | socket.AI_V4MAPPED | socket.AI_CANONNAME) #从DNS服务器获取IP地址
    except socket.gaierror as exc:
        print('name service failure:', exc.args[1])
        sys.exit(1)

    info = infolist[0]
    socket_args = info[0:3]
    address = info[4]
    sock = socket.socket(*socket_args)
    try:
        sock.connect(address) #尝试连接该IP地址
    except socket.error as exc:
        print('network failure:', exc.args[1])
    else:
        print('success: host', info[3], 'is listening on port 80') #连接成功的话，会显示该IP地址的规范主机名

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='try connecting to port 80')
    parser.add_argument('hostname', help='hostname that you want to contact')
    connect_to(parser.parse_args().hostname)
