"""《流畅的python》中的示例 18-8：使用命令行参数和事件循环，异步下载多个国家的国旗"""
import asyncio
import collections
import aiohttp
from aiohttp import web
from tqdm import tqdm
from flags2_common import main, HTTPStatus, Result, save_flag

#默认设为较小的值，防止远程网站出错，例如503 error
DEFAULT_CONCUR_REQ = 5
MAX_CONCUR_REQ = 1000

class FetchError(Exception):
    """自定义的异常类"""
    def __init__(self, country_code):
        self.country_code = country_code

async def get_flag(base_url, cc):
    """三级被调协程，连接目标网站，发送http请求，根据不同的状态码，抓取内容或者抛出异常"""
    url = '{}/{}/{}.gif'.format(base_url, cc.lower(), cc.lower())
    async with aiohttp.ClientSession() as session:
        resp = await session.get(url) #发送http请求
        if resp.status == 200:
            image = await resp.read() #抓取网页内容
            return image
        elif resp.status == 404:
            raise web.HTTPNotFound()
        else:
            raise aiohttp.web.HttpProcessingError(code=resp.status, message=resp.reason, headers=resp.headers)

async def download_one(cc, base_url, semaphore, verbose):
    """二级被调协程，驱动get_flag()协程，并根据后者的行为，保存抓取的内容，或者处理并记录后者抛出的异常"""
    try:
        async with semaphore: #信号量用于向worker（协程）定额分配共享的资源，相当于N把lock，用于限制可以同时/异步执行的协程数量
            image = await get_flag(base_url, cc)
    except web.HTTPNotFound:
        status = HTTPStatus.not_found #是个枚举成员
        msg = 'not found'
    except Exception as exc:
        raise FetchError(cc) from exc #显式异常链，exc异常被链接为FetchError()异常对象的__cause__属性
    else:
        loop=asyncio.get_event_loop() #获取当前的事件循环对象
        await loop.run_in_executor(None, save_flag, image, cc.lower()+'.gif') #通过事件循环维护线程池，并发执行save_flag()这个I/O函数
        #save_flag(image, cc.lower()+'.gif') #不用线程池并发保存的版本，以供对比

        status = HTTPStatus.ok #是个枚举成员
        msg = 'OK'
    if verbose and msg:
        print(cc, msg)
    return Result(status, cc) #返回一个记录了单个任务完成状态的具名元组

async def download_coro(cc_list, base_url, verbose, concur_req):
    """一级被调协程，负责创建并委派所有的下载任务/task，并对每个task的完成状态进行统计"""
    counter = collections.Counter() #创建一个计数器，能够根据download_one()协程返回的具名元组，统计任务下载成功、未找到、网络错误的次数
    semaphore = asyncio.Semaphore(concur_req) #创建一个信号量，它会被所有的download_one()协程共享
    to_do = [download_one(cc, base_url, semaphore, verbose) for cc in sorted(cc_list)] #批量创建download_one()协程，每个协程代表一个下载任务

    to_do_iter = asyncio.as_completed(to_do) #返回一个由所有task对象组成的迭代器，该迭代器中的task对象，基于任务完成的先后顺序进行排列
    if not verbose:
        to_do_iter = tqdm(to_do_iter, total=len(cc_list))
    for future in to_do_iter:
        try:
            res = await future #task/future对象的返回值，就是Result()具名元组
        except FetchError as exc: #捕获download_one()协程中抛出的异常
            country_code = exc.country_code
            try:
                error_msg = exc.__cause__.args[0] #尝试从原来的异常（__cause__）中获取错误消息，即exc value
            except IndexError: #如果获取exc value失败
                error_msg = exc.__cause__.__class__.__name__ #转而从原来的异常（__cause__）中获取exc type
            if verbose and error_msg:
                print('*** Error for {}: {}'.format(country_code, error_msg))
            status = HTTPStatus.error #是个枚举成员
        else:
            status = res.status #如果try子句未捕获到FetchError异常，则直接继承download_one()协程返回的具名元组记录的status，即HTTPStatus.ok和HTTPStatus.not_fount
        counter[status] += 1 #分别统计3种status出现的的次数
    return counter

def download_many(cc_list, base_url, verbose, concur_req):
    """事件循环所在的的最外层，是个普通函数"""
    loop = asyncio.get_event_loop()
    coro = download_coro(cc_list, base_url, verbose, concur_req)
    counts = loop.run_until_complete(coro)
    loop.close()
    return counts

if __name__ == "__main__":
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)




def stage3(response3):
    """三级被调函数"""
    step3(response3)

def stage2(response2):
    """二级被调函数"""
    request3=step2(response2)
    api_call3(request3, stage3)

def stage1(response1):
    """一级被调函数"""
    request2=step(response1)
    api_call2(request2, stage2)

api_call1(request1, stage1)


