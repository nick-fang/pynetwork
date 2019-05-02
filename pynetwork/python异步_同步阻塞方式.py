"""深入理解python异步编程-同步阻塞方式"""
import socket
import time

def blocking_way():
    """阻塞的socket连接和传输"""
    sock = socket.socket()
    sock.connect(('example.com', 80)) #阻塞
    request = 'GET / HTTP/1.0\r\nHost: example.com\r\n\r\n'
    sock.send(request.encode('ascii')) #发送请求报文
    response = b''
    chunk = sock.recv(4096) #阻塞，先接收4096字节的响应流
    while chunk:
        response += chunk #拼接响应报文
        chunk = sock.recv(4096) #阻塞，每次接收4096字节的响应流
    return response #返回拼接好的响应报文

def sync_way():
    res = []
    for i in range(10): #尝试下载example.com首页10次
        res.append(blocking_way())
        print(f'task {i}: completed.')
    return len(res)

start = time.time()
print(sync_way())
end = time.time()
print('consumed {:.2f} secs'.format(end - start))
