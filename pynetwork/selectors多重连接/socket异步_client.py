"""使用selectors模块构建异步TCP服务器：echo-server"""
import selectors
import socket
import argparse
sel = selectors.DefaultSelector()
messages = [b'beautiful is better than ugly.', 
            b'simple is better than complex.']
msg_total = sum(len(msg) for msg in messages) #待发送的2条消息字节串的总长度

def service_connection(key, mask):
    """连接套接字写就绪时：向服务器端发送请求数据；连接套接字读就绪时：接收服务器端的响应数据"""
    sock = key.fileobj
    connid = key.data['connid']
    msgs = key.data['messages']
    if mask & selectors.EVENT_READ: #如果读就绪
        data = sock.recv(1024)
        if data:
            print('>>> received {!r} from connection {}'.format(data, connid))
            key.data['bytes_recv'] += len(data)
        if key.data['bytes_recv'] == msg_total: #如果接收到了全部的消息；这里无法依靠服务器端的空字节串，因为客户端应该比服务器端先关闭连接套接字
            print('closing connection {}'.format(connid))
            sel.unregister(sock) #从选择器中注销该套接字
            sock.close() #关闭连接套接字；从而服务器端也能正常关闭连接套接字
    if mask & selectors.EVENT_WRITE: #如果写就绪
        if msgs: #如果消息列表中还有数据
            msg = msgs.pop(0) #从列表中取出1条待发送的消息
            print('>>> sending {!r} to connection {}'.format(msg, connid))
            sock.sendall(msg)

def start_connection(host, port, num_conns):
    """向服务器端发起复数个连接请求"""
    for connid in range(1, num_conns+1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex((host, port)) #行为类似connect函数，但是网络出错时不抛出异常，而是返回一个状态码
        print('starting connection {} to {}'.format(connid, sock.getpeername()))
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = {'connid':connid, 'bytes_recv':0, 'messages':list(messages)}
        sel.register(sock, events, data=data) #向sel选择器注册文件对象sock，以监视它的【读|写就绪事件】;因为是在for循环中，所以这里注册了多个连接套接字，而后者的send和recv能在接下来的事件循环中异步执行

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='multiconn-client based on selectors module')
    parser.add_argument('-n', metavar='hostname', default='127.0.0.1')
    parser.add_argument('-p', metavar='port', type=int, default=65432)
    parser.add_argument('-c', metavar='num_connections', type=int, default=3)
    args = parser.parse_args()
    start_connection(args.n, args.p, args.c) #发起的连接数默认为3

    while True: #事件监视循环
        events = sel.select(timeout=None) #阻塞模式
        for key, mask in events:
            service_connection(key, mask) #异步执行多个该函数
        if not sel.get_map(): #选择器中的fileobj全部注销掉了
            break
    sel.close()
