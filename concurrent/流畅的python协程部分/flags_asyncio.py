
import asyncio
import aiohttp
from flags import BASE_URL, save_flag, show, main

async def get_flag(cc):
    """二级被调协程"""
    url = '{}/{}/{}.gif'.format(BASE_URL, cc.lower(), cc.lower())
    async with aiohttp.ClientSession() as session: #通过新版aiohttp包进行HTTP操作前，首先必须开启一个会话/session；session负责保持一次TCP连接的keep-alive状态和cookies
        resp = await session.get(url) #get方法返回一个协程
        image = await resp.read() #read方法返回一个协程
    return image

async def download_one(cc):
    """一级被调协程，代表一项下载任务"""
    image = await get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc

def download_many(cc_list):
    loop = asyncio.get_event_loop()
    to_do = [download_one(cc) for cc in sorted(cc_list)] #一个由协程对象组成的列表
    wait_coro = asyncio.wait(to_do) #wait是个协程函数，调用后返回一个协程；后者在被驱动后，能够批量创建task对象，并将后者加入到当前的事件循环中，从而异步执行这些task
    res, _ = loop.run_until_complete(wait_coro) #使用事件循环驱动wait函数返回的协程对象，后者的返回值是个由两个集合组成的元组，这里通过元组拆包获取第一个集合，列举了已完成的task
    loop.close()
    return len(res) #已完成的下载任务的数量

if __name__ == "__main__":
    main(download_many)
