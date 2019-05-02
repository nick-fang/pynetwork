"""使用selectors模块构建异步TCP服务器：echo-server"""
import selectors
import socket
sel = selectors.DefaultSelector()

def service_connection(key, mask):
    """连接套接字读就绪时：接收客户端的数据，并原样发送回去"""
    sock = key.fileobj
    bytes_recv = b'' #因为函数中定义的局部变量互不影响，所以每个连接套接字都独有一个bytes_recv变量
    if mask & selectors.EVENT_READ:
        data = sock.recv(1024)
        if not data: #如果客户端关闭了连接套接字
            print('closing connection to', sock.getpeername())
            sel.unregister(sock) #从选择器中注销该连接套接字
            sock.close() #服务器端在客户端之后，关闭连接套接字
        else:
            print('>>> echoing', repr(data), 'to', sock.getpeername())
            sock.sendall(data)

def accept_wrapper(sock):
    """监听套接字读就绪时：接收客户端的连接请求，创建连接套接字"""
    conn, addr = sock.accept()
    print('accepted connection from', addr)
    conn.setblocking(False) #将【连接套接字】设置为非阻塞
    sel.register(conn, selectors.EVENT_READ, data='connect')

if __name__ == "__main__":
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind(('127.0.0.1', 65432))
    lsock.listen()
    print('listening at', lsock.getsockname())
    lsock.setblocking(False) #将【监听套接字】设置为非阻塞
    sel.register(lsock, selectors.EVENT_READ, data='listen')

    while True: #事件监视循环
        events = sel.select(timeout=None) #阻塞模式
        for key, mask in events:
            if key.data == 'listen': #如果是监听套接字的事件；注意在上面的函数中，监听套接字并未从选择器中注销，所以这个事件会一直存在
                accept_wrapper(key.fileobj) #异步执行多个该函数
            elif key.data == 'connect': #如果是连接套接字的事件
                service_connection(key, mask) #异步执行多个该函数
