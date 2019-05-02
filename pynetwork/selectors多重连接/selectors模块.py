"""使用selectors模块构造的一个异步TCP服务器：echo whatever it receives back to the client."""
import selectors
import socket

sel = selectors.DefaultSelector() #创建一个selector对象，Windows默认调用select()

def read(conn, mask):
    """客户端发送的数据到达服务器端，后者的连接套接字读就绪时，触发的回调"""
    data = conn.recv(1024) #这是连接套接字的一项【读操作】
    if data: #如果接收到了数据
        print('echoing', repr(data), 'to', conn)
        conn.send(data) #这是连接套接字的一项【写操作】
    else: #如果接收到了空字节串，表示客户端关闭了连接
        print('closing', conn)
        sel.unregister(conn) #从选择器中注销掉该连接套接字
        conn.close()

def accept(sock, mask): #mask参数有什么用？？
    """客户端的连接请求到达服务器端，后者的监听套接字读就绪时，触发的回调"""
    conn, addr = sock.accept() #这是监听套接字的一项【读操作】
    print('accepted', conn, 'from', addr)
    conn.setblocking(False) #将服务器端的【连接套接字】设置为非阻塞
    sel.register(conn, selectors.EVENT_READ, read) #向sel选择器注册文件对象conn，以监视它的【读就绪事件】

sock = socket.socket()
sock.bind(('localhost', 1060))
sock.listen(100)
sock.setblocking(False) #将服务器端的【监听套接字】设置为非阻塞
print('listening at', sock.getsockname())
sel.register(sock, selectors.EVENT_READ, accept) #向sel选择器注册文件对象sock，以监视它的【读就绪事件】

while True:
    events = sel.select() #events是个由(key, mask)元组构成的迭代器
    for key, mask in events: #从选择器中一一获取就绪的任务
        callback = key.data #从selectorkey对象中取出事先注册的回调函数名
        callback(key.fileobj, mask) #手动调用事先注册的回调调函
