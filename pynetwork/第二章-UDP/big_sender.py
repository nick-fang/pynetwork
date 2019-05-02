"""代码清单2-3 发送大型UDP数据报；该脚本仅适用于Linux系统"""
import argparse
import socket
import sys
# Inlined constants, because Python 3.6 has dropped the IN module.
class IN:
    IP_MTU = 14
    IP_MTU_DISCOVER = 10
    IP_PMTUDISC_DO = 2

if sys.platform != 'linux':
    print('Unsupported: Can only perform MTU discovery on Linux',
          file=sys.stderr)
    sys.exit(1)

def send_big_datagram(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.IPPROTO_IP, IN.IP_MTU_DISCOVER, IN.IP_PMTUDISC_DO) #设置套接字选项，关闭UDP套接字的自动分组功能？？
    sock.connect((host, port))
    try:
        sock.send(b'#' * 999999) #尝试发送一个超大的UDP数据报
    except socket.error:
        print('Alas, the datagram did not make it')
        max_mtu = sock.getsockopt(socket.IPPROTO_IP, IN.IP_MTU) #查询当前Linux系统支持的MTU
        print('Actual MTU: {}'.format(max_mtu))
    else:
        print('The big datagram was sent!')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send UDP packet to get MTU')
    parser.add_argument('host', help='the host to which to target the packet')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='UDP port (default 1060)')
    args = parser.parse_args()
    send_big_datagram(args.host, args.p)
