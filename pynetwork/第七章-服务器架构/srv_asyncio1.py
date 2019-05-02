"""代码清单7-7 回调风格的asyncio服务器，python3.7才能使用"""
import asyncio
import zen_utils

class ZenServer(asyncio.Protocol):
    def connection_made(self, transport): #transport object是什么东西？？类似一个连接套接字？？
        """负责连接套接字建立后的准备工作"""
        self.transport = transport
        self.address = transport.get_extra_info('peername') #获取连接套接字的远端地址
        self.data = b''
        print('accepted connection from {}'.format(self.address))

    def data_received(self, data):
        """负责数据的接收、处理和发送，可以会被调用多次"""
        self.data+=data
        if self.data.endswith(b'?'):
            answer = zen_utils.get_answer(self.data)
            self.transport.write(answer)
            self.data = b''

    def connection_lost(self, exc):
        """负责一次连接结束后的清理工作"""
        if exc:
            print('client {} error: {}'.format(self.address, exc))
        elif self.data:
            print('client {} sent {} but then closed'.format(self.address, self.data))
        else:
            print('client {} closed socket'.format(self.address))

async def main():
    """一个异步TCP服务器"""
    address = zen_utils.parse_command_line('asyncio server using callback') #从命令行获取(IP, port)元组
    server = await loop.create_server(ZenServer, *address) #返回一个server对象
    addr = server.sockets[0].getsockname() #获取该server对象上的监听套接字所绑定的地址
    print(f'serving on {addr}')
    async with server: #确保server对象能够顺利关闭；python3.7才能使用的代码
        await server.serve_forever() #持续监听并接收新请求

if __name__=="__main__":
    loop = asyncio.get_event_loop() #创建一个事件循环
    try:
        loop.run_until_complete(main()) #驱动main()协程
    finally:
        loop.close()
