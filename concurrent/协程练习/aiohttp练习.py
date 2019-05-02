import aiohttp
import asyncio
import async_timeout
import os

async def download_coroutine(session, url):
    """单个下载任务"""
    with async_timeout.timeout(10):
        async with session.get(url) as response: #下载异步
            filename = os.path.basename(url) #待下载的pdf文件名
            with open('pdfs\\' + filename, 'wb') as f_handle:
                while True:
                    chunk = await response.content.read(1024) #读取下载数据异步
                    if not chunk:
                        break
                    f_handle.write(chunk) #磁盘写入
                return await response.release() #上下文管理器的清理工作，可省略；async with结构中，异步await发生在退出时的清理工作？？
async def main(loop):
    urls = ["http://www.irs.gov/pub/irs-pdf/f1040.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040a.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040ez.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040es.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040sb.pdf"]

    async with aiohttp.ClientSession(loop=loop) as session:
        tasks = [download_coroutine(session, url) for url in urls] #多个下载任务/协程对象组成的列表
        await asyncio.gather(*tasks) #等待多个下载任务组成的future聚合体
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
    print('pdfs download finished.')







import asyncio
import aiohttp

async def fetch(session, url):
    """二级被调协程"""
    async with session.get(url) as response:
        return await response.text()

async def main():
    """一级被调协程"""
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, 'http://python.org')
        print(html)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())




import aiohttp
#相比requests库，多了创建session这一步，且async with操作必须放进协程函数中
async def main():
    """主逻辑是个协程函数，意味着还需要在外层使用事件循环驱动它返回的协程对象"""
    async with aiohttp.ClientSession() as session: #几乎相当于【session = await aiohttp.Clientsession().__aenter__()】，该方法【调用后返回的协程对象的返回值】正好是对象自身，所以实际相当于【session = aiohttp.Clientsession()】
        async with session.get('http://httpbin.org/get') as resp: #相当于【resp = await session.get('http://httpbin.org/get').__aenter__()】，该方法返回的是self._resp，所以实际相当于【resp = session.get('http://httpbin.org/get')._resp】
            print(resp.status)
            print(await resp.text()) #可以认为，aiohttp库中的函数几乎都是协程函数，不是用事件循环或await驱动，就是用async with驱动



"""Client Session
ClientSession is the heart and the main entry point for all client API operations.
Create the session first, use the instance for performing HTTP requests and initiating WebSocket connections.
The session contains a cookie storage and connection pool, thus cookies and connections are shared between HTTP requests sent by the same session."""

#设定超时，aiohttp session的超时默认为5min
#即：aiohttp.ClientTimeout(total=5*60, connect=None, sock_connect=None, sock_read=None)
async def main():
    timeout = aiohttp.ClientTimeout(total=60) #60sec
    async with aiohttp.ClientSession(timeout=timeout) as session:
        pass



#状态码、文本、二进制内容、json解码内容
async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://api.github.com/events') as resp:
            print(resp.status)
            print(await resp.text(encoding='windows-1251'))
            print(await resp.read()) #相当于requests库的resp.content
            print(await resp.json()) #注意，服务器响应数据正好是json格式时，resp.json()方法才会解码成功，否则会触发异常


#传递http命令参数
async def main():
    async with aiohttp.ClientSession() as session:
        params={'key1': 'value1', 'key2': 'value2'}
        async with session.get('http://httpbin.org/get', params=params) as resp:
            expect='http://httpbin.org/get?key2=value2&key1=value1'
            assert str(resp.url)==expect



#流式下载，相当于requests库的resp.iter_content()方法
async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://api.github.com/events') as resp:
            with open(filename, 'wb') as fout:
                while True:
                    chunk=await resp.content.read(chunk_size)  #resp.content，代表【流响应内容】
                    if not chunk:
                        break
                    fout.write(chunk)



#使用字符串，或二进制数据进行POST请求
async def main():
    async with aiohttp.ClientSession() as session:
        async with session.post('http://httpbin.org/post', data=b'\x00Binary-data\x00') as resp: #data也可以是个字符串
            pass


#使用json数据进行POST请求
async def main():
    async with aiohttp.ClientSession() as session:
        payload={'key1': 'value1', 'key2': 'value2'}
        async with session.post('http://httpbin.org/post', json=payload): #该网址，能够把我们的POST请求报文，作为响应内容返回回来
            print(await resp.text())


#使用磁盘上的文件（office文档、图片等），进行POST请求
async def main():
    async with aiohttp.ClientSession() as session:
        data=aiohttp.FormData() #创建一个表单，用于存储该文件的相关信息
        data.add_field('file', 
                       open('report.xls', 'rb'), 
                       filename='report.xls', 
                       content_type='application/vnd.ms-excel')
        await session.post(url, data=data)


import aiofiles
#流式上传
async def file_sender(file_name=None):
    """这是一个异步生成器函数"""
    async with aiofiles.open(file_name, 'rb') as fin:
        chunk=await fin.read(64*1024)
        while chunk:
            yield chunk #该函数的功能是：惰性产出chunk
            chunk=await fin.read(64*1024)

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.post('http://httpbin.org/post', data=file_sender(file_name='huge_file')) as resp:
            print(await resp.text())



#GET：使用代理服务器连接目标网站
async def main():
    async with aiohttp.ClientSession() as session:
        proxy_auth=aiohttp.BasicAuth('user', 'pass') #创建一个用于保存代理服务器登录信息的表单；如果代理服务器无需登录，则该条语句可以省略
        async with session.get('http://python.org', proxy='http://proxy.com', proxy_auth=proxy_auth) as resp:
            print(resp.status)


#GET：向目标网站发送自定义cookies
async def main():
    cookies={'cookies_are':'working'}
    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.get('http://httpbin.org/cookies') as resp: #该网址会把请求报文的cookies，作为响应报文返回
            print(await resp.json()) #返回的cookies是json格式



"""一个POST请求的示例"""
import asyncio
import aiohttp
from pprint import pprint

async def main():
    payload=b'GIF89a\x01\x00\x01\x00\x00\xff\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x00;' #上传一张gif图片
    headers={'content-type':'image/gif'} #在请求报文首部添加自定义字段
    timeout=aiohttp.ClientTimeout(total=60) #设置超时为60秒
    async with aiohttp.ClientSession(timeout=timeout) as session:
        resp=await session.post('http://httpbin.org/post', data=payload, headers=headers) #该网址会将请求报文，作为响应报文返回
        pprint(await resp.text()) #打印响应报文的内容

loop=asyncio.get_event_loop()
loop.run_until_complete(main())

