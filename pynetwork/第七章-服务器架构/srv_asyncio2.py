"""代码清单7-8 协程风格的asyncio服务器，python3.7才能使用"""
import asyncio
import zen_utils

async def handle_conversation(reader, writer):
    """负责一个连接套接字的会话"""
    address = writer.get_extra_info('peername') #获取writer对象的底层连接套接字的远端地址，即发出该次请求的客户端的地址
    print('accepted connection from {}'.format(address))
    while True: #持续【接收问题，发送答案】的循环，直到客户端关闭连接套接字为止
        try:
            data = await reader.readuntil(b'?') #从接收缓冲区持续读取字节串，直到遇到【?】为止
        except asyncio.IncompleteReadError: #如果遇到了EOF信号，即远端关闭了套接字，则退出协程函数
            break
        answer = zen_utils.get_answer(data)
        writer.write(answer) #将答案写入发送缓冲区
        await writer.drain() #控制write()方法写入的流量
    print('close the connection')
    writer.close() #关闭writer底层的服务器连接套接字

#if __name__ == "__main__":
#    address = zen_utils.parse_command_line('asyncio server using coroutine')
#    loop = asyncio.get_event_loop()
#    coro = asyncio.start_server(handle_conversation, *address)
#    server = loop.run_until_complete(coro) #coro会被排定为一个task
#    print('listening at {}'.format(address))
#    try:
#        loop.run_forever() #python3.6的代码，使用loop的方法来驱动server
#    finally:
#        server.close()
#        loop.close()

async def main():
    address = zen_utils.parse_command_line('asyncio server using coroutine')
    server=await asyncio.start_server(handle_conversation, *address)
    print('listening at {}'.format(address))
    async with server: #确保server对象能够顺利关闭；python3.7才能使用的代码
        await server.serve_forever() #持续监听并接收新请求

if __name__=="__main__":
    loop = asyncio.get_event_loop() #创建一个事件循环
    try:
        loop.run_until_complete(main()) #驱动main()协程
    finally:
        loop.close()
