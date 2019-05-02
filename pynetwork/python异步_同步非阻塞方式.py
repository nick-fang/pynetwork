"""深入理解python异步编程-非阻塞方式"""
import socket
import time

def nonblocking_way():
    """非阻塞的socket连接和传输"""
    sock = socket.socket()
    sock.setblocking(False) #将该sock对象的所有方法设置为非阻塞
    try:
        sock.connect(('example.com', 80))
    except BlockingIOError: #无论阻塞（比如设置了超时）还是非阻塞模式，只要连接未完成就被强制返回，操作系统低层就会抛出该异常；所以非阻塞模式下几乎肯定辉抛出该异常
        pass
    request = 'GET / HTTP/1.0\r\nHost: example.com\r\n\r\n'
    data = request.encode('ascii')
    while True: #不知道socket何时就绪/连接完毕，所以这里不断尝试发送请求报文
        try:
            sock.send(data) #如果未连接成功就发出数据，会触发OSError异常，于是进入下面的except子句
            break #直到send不抛出异常，则发送完毕，跳出循环
        except OSError:
            pass

    response = b''
    while True:
        try:
            chunk = sock.recv(4096) #recv调用也不会再阻塞，如果不能立即接收到响应报文(可能时连接还未成功，也可能是服务器端发送的响应报文还在路上，还可能是该响应报文丢包了)，则强制返回并触发OSError异常
            while chunk:
                response += chunk
                chunk = sock.recv(4096) #接收完响应报文后，再次调用recv会发现连接的远程端关闭，于是返回一个空字节串赋值给chunk，从而退出内层while循环
            break #这个break语句，用于跳出最外层的while循环，然后函数return
        except OSError:
            pass
    return response

def sync_way():
    res = []
    for i in range(10):
        res.append(nonblocking_way())
        print(f'task {i}: completed.')
    return len(res)

start = time.time()
print(sync_way())
end = time.time()
print('consumed {:.2f} secs'.format(end - start))
