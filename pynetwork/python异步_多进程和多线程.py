"""深入理解python异步编程-进程/线程池方式"""
import socket
import time
from concurrent import futures

def blocking_way(task_No):
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
    print(f'task {task_No}: completed.')
    return response #返回拼接好的响应报文

def process_way():
    """方案1：进程池；方案2：线程池"""
    #with futures.ProcessPoolExecutor(max_workers=10) as executor:
    with futures.ThreadPoolExecutor(max_workers=10) as executor:
        futs = [executor.submit(blocking_way, i) for i in range(10)]
        res = [fut.result() for fut in futs]
    return len(res)

if __name__ == "__main__":
    start = time.time()
    print(process_way())
    end = time.time()
    print('consumed {:.2f} secs'.format(end - start))
