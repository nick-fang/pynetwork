#import asyncio

#async def tcp_echo_client(message):
#    """是个协程函数，包含TCP客户端的所有逻辑；参数是要发送出去的消息"""
#    reader, writer = await asyncio.open_connection('127.0.0.1', 8888) #客户端连接套接字的接收侧和发送侧

#    print(f'send: {message!r}')
#    writer.write(message.encode()) #发送不会阻塞，因此没有必要使用await

#    data = await reader.read(100) #等待接收服务器端处理，并发回来的消息
#    print(f'received: {data.decode()!r}')

#    print('close the connection')
#    writer.close() #关闭writer对象底层的连接套接字
#    await writer.wait_closed() #该方法Should be called after close() to wait until the underlying connection is closed.

#asyncio.run(tcp_echo_client('hello world!'))






"""asyncio异步客户端：获取HTTP headers"""
import asyncio
import urllib.parse
import sys

async def print_http_headers(url):
    url = urllib.parse.urlsplit(url)
    if url.scheme == 'https':
        reader, writer = await asyncio.open_connection(url.hostname, 443, ssl=True)
    else:
        reader, writer = await asyncio.open_connection(url.hostname, 80)

    query = (f"HEAD {url.path or '/'} HTTP/1.0\r\n"
             f"Host: {url.hostname}\r\n"
             f"\r\n") #一个HEAD请求的请求头；【url.path or '/'】是为了防止待解析的ulr主页漏写了末尾的【/】

    writer.write(query.encode('latin-1')) #发送请求
    while True:
        line = await reader.readline() #等待接收响应
        if not line: #如果读到EOF信号，则退出循环
            break
        line = line.decode('latin-1').rstrip()
        if line:
            print(f'HTTP header> {line}') #将接收到的响应头，逐行打印出来

    writer.close() #关闭writer对象底层的连接套接字

url = sys.argv[1]
asyncio.run(print_http_headers(url))

