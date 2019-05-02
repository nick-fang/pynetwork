"""可能造成死锁的TCP服务器和客户端"""
import argparse
import socket
import sys

def server(host, port, bytecount):
    """服务器端；bytecount变量未使用，是为了配合命令行参数的统一，而被强行放在这里"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #双方四次挥手后不再等待4分钟才彻底断开连接，仅Linux下有效
    sock.bind((host, port))
    sock.listen(1)
    print('listening at', sock.getsockname())
    while True: #负责监听客户端连接请求的循环
        conn, sockname = sock.accept()
        print('processing up to 1024 bytes at a time from', sockname)
        sent = 0
        while True: #服务器端的接收与发送放在了同一个循环中
            data = conn.recv(1024) #尝试接收1024字节，但未必能够全部接收到
            if not data: #如果客户端发送完毕并关闭它的套接字（实际这里客户端只是通过shutdown()方法关闭了发送方向的通信），则服务器端会收到空字节串，于是跳出循环
                break
            output = data.decode('ascii').upper().encode('ascii') #转字符串转大写，再转回字节串
            conn.sendall(output) #将大写的字节串全部发送回客户端
            sent += len(data) #记录服务器端已经发送出去的字节数
            print('\r  {} bytes processed so far'.format(sent), end=' ') #\r是回车符，表示回到行首，从而能够在同一位置刷新输出【已发送的字节数】
            sys.stdout.flush() #强制刷新终端窗口的输出
        print() #手动换行
        conn.close()
        print('  socket closed')

def client(host, port, bytecount):
    """客户端"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bytecount = (bytecount + 15) // 16 * 16 #向后取最近的一个16的倍数
    message = b'capitalize this!' #正好16个字节
    print('sending', bytecount, 'bytes of data, in chunks of 16 bytes')
    sock.connect((host, port)) #尝试连接服务器
    sent = 0
    while sent < bytecount: #客户端总共要向服务器端发送bytecount字节的数据，即(bytecount//16)个message
        sock.sendall(message) #将一个message全部发送给服务器端
        sent += len(message) #记录客户端已经发送出去的字节数
        print('\r  {} bytes sent'.format(sent), end=' ') #\r是回车符，表示回到行首，从而能够在同一位置刷新输出【已发送的字节数】
        sys.stdout.flush() #强制刷新终端窗口的输出
    print() #手动换行
    sock.shutdown(socket.SHUT_WR) #关闭客户端【发送方向】的通信，即告知服务器端自己不再发送数据，服务器端会如同遇到了文件结束符（即客户端的close()调用）一样，接收到一个空字节串
    print('receiving all the data the server sends back')

    received = 0
    while True:
        data = sock.recv(42) #尝试接收42字节，但未必能够全部接收到；为什么是42？？？
        if not received: #只有第一次循环会进入该条件语句
            print('  the first data received says', repr(data))
        if not data: #如果服务器端发送完毕并关闭它的套接字，则客户端会收到空字节串，于是跳出循环
            break
        received += len(data) #记录客户端已经接收到的字节数
        print('\r  {} bytes received'.format(received), end=' ')
    print() #手动换行
    sock.close()

if __name__ == "__main__":
    CHOICES = {'client':client, 'server':server}
    parser = argparse.ArgumentParser(description='get deadlocked over TCP')
    parser.add_argument('role', choices=CHOICES, help='which role to play')
    parser.add_argument('host', help='interface the server listens at; host the client sends to')
    parser.add_argument('bytecount', type=int, nargs='?', default=16, help='number of bytes for client to send(default 16)') #nargs='?'表示即使该命令行参数未提供，它也会存在，且值为16
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='TCP prot (default 1060)')
    args = parser.parse_args()
    function = CHOICES[args.role]
    function(args.host, args.p, args.bytecount)
