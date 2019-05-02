
import asyncio

async def main():
    print('hello')
    await asyncio.sleep(1)
    print('world')

asyncio.run(main())



import asyncio
import time

async def say_after(delay, what):
    """二级被调协程"""
    await asyncio.sleep(delay)
    print(what)

async def main():
    """一级被调协程，用来驱动二级被调协程"""
    print('started at', time.strftime('%X'))
    await say_after(1, 'hello')
    await say_after(2, 'world')
    print('finished at', time.strftime('%X'))

asyncio.run(main()) #run函数，用来驱动一级被调协程

async def say_after(delay, what):
    """二级被调协程"""
    await asyncio.sleep(delay)
    print(what)

async def main():
    """将二级被调协程封装成task对象，然后驱动后者"""
    task1 = asyncio.create_task(say_after(1, 'hello'))
    task2 = asyncio.create_task(say_after(2, 'world'))
    print('started at', time.strftime('%X'))
    await task1
    await task2
    print('finished at', time.strftime('%X'))

asyncio.run(main())



import asyncio

async def nested():
    return 42

async def main():
    nested() #这条语句啥也不会做
    print(await nested()) #使用await驱动后，打印出“42”
asyncio.run(main())




import asyncio

async def nested():
    return 42

async def main():
    task = asyncio.create_task(nested()) #封装成task，也能像await关键字一样，驱动协程对象
    print(task)
    await task #等待task执行完毕，就像线程池的future.result()方法，或者线程对象的thread.join()方法，完成前会阻塞调用方？？这里await的作用就是“等待”，而非“驱动”了
    print(task)

asyncio.run(main())



import asyncio

async def main():
    await function_that_returns_a_future_object()

    await asyncio.gather(function_that_returns_a_future_object(),
                         some_python_coroutine())

asyncio.run(main())




import asyncio
import datetime

async def display_date():
    loop = asyncio.get_running_loop() #搜寻并返回当前正在运转的事件循环
    end_time = loop.time() + 5.0
    while True:
        if loop.time() >= end_time: #+0、+1、+2、+3、+4，共5次
            break
        print(datetime.datetime.now())
        await asyncio.sleep(1) #每阻塞1秒，loop.time()的值就+1
asyncio.run(display_date())




import asyncio

async def factorial(name, number):
    """计算阶乘的协程函数"""
    fact = 1
    for i in range(2, number + 1):
        print(f"task {name}: compute factorial({i})...") #打印计算步骤
        await asyncio.sleep(1)
        fact*=i
    print(f"task {name}: factorial({number}) = {fact}") #打印计算结果
    return fact #将计算结果作为协程对象的返回值

async def main():
    """并发地排定3个协程对象"""
    tasks = asyncio.gather(factorial('A', 2), factorial('B', 3), factorial('C', 4)) #返回一个协程对象
    result = await tasks #使用await驱动协程对象，同时使用result变量接收该协程对象的返回值
    print('aggregate list of returned values is:', result)

asyncio.run(main())



import asyncio

async def eternity():
    """二级被调协程，休眠1个小时"""
    await asyncio.sleep(3600)
    print('yay!')

async def main():
    """一级被调协程，等待最多1秒"""
    try:
        await asyncio.wait_for(eternity(), timeout=1.0)
    except asyncio.TimeoutError:
        print('timeout!')

asyncio.run(main())



import asyncio
from pprint import pprint

async def do_some_work(x):
    """二级被调协程"""
    print(f'waiting asyncio.sleep({x})...')
    await asyncio.sleep(x)
    print(f'work{x} done')

async def main():
    """一级被调协程"""
    result = await asyncio.wait([do_some_work(1), 
                                 do_some_work(3)])
    pprint(result)

asyncio.run(main())





import asyncio
from pprint import pprint

async def nested():
    """二级被调协程"""
    return 42

async def main():
    """一级被调协程"""
    task = asyncio.create_task(nested()) #封装成task，也能像await关键字一样，驱动协程对象
    pprint(asyncio.current_task())
    pprint(asyncio.all_tasks())
    await task

asyncio.run(main())



import asyncio

async def cancel_me():
    print('cancel_me(): before sleep')
    try:
        await asyncio.sleep(3600) #等待1个小时
    except asyncio.CancelledError: #捕获【取消错误异常】
        print('cancel_me(): cancel sleep')
        raise #重新触发捕获的【取消错误】异常
    finally:
        print('cancel_me(): after sleep')

async def main():
    task=asyncio.create_task(cancel_me()) #从创建cancel_me()的task开始，事件循环中就同时存在main()和cancel_me()这2个task了
    await asyncio.sleep(1) #main()协程中断1秒，控制权移交给cancel_me()协程
    task.cancel() #等待1秒后，就取消task
    try:
        await task #等待task，此时控制权又一次移交给cancel_me()协程，然后【取消错误】异常才会在该协程中冒泡
    except asyncio.CancelledError: #cancel_me()内部的【取消错误】异常向上冒泡，然后被main()此处的代码捕获
        print('main(): cancel_me is cancelled now')

asyncio.run(main())



import asyncio

async def cancel_me():
    print('cancel_me() started.')
    await asyncio.sleep(3600) #等待1个小时

async def main():
    task=asyncio.create_task(cancel_me()) #从创建cancel_me()的task开始，事件循环中就同时存在main()和cancel_me()这2个task了
    await asyncio.sleep(1) #main()协程中断1秒，控制权移交给cancel_me()协程
    task.cancel() #等待1秒后，就取消task
    try:
        await task #等待task，此时控制权又一次移交给cancel_me()协程，然后【取消错误】异常才会在该协程中冒泡
    except asyncio.CancelledError: #这里忽略掉冒到main()协程中的异常，才能继续执行后面状态检查
        pass
    print('cancel_me is cancelled? ',task.cancelled())

asyncio.run(main())



"""为future添加回调"""
import asyncio
async def do_some_work(x):
    """一个协程"""
    print(f'waiting asyncio.sleep({x})...')
    await asyncio.sleep(x)

def done_callback(future):
    """被回调的函数"""
    print('done')

loop=asyncio.get_event_loop() #创建事件循环
future=asyncio.ensure_future(do_some_work(3)) #将协程封装成future对象
future.add_done_callback(done_callback) #为future对象添加回调功能
loop.run_until_complete(future) #通过事件循环调用future对象

loop=asyncio.get_event_loop() #创建事件循环
futures=asyncio.gather(do_some_work(1), do_some_work(3))
futures.add_done_callback(done_callback)
loop.run_until_complete(futures) #gather()协程返回的聚合列表，会返回到它的驱动/调用方



"""需要python3.7支持"""
import asyncio
import concurrent.futures

def blocking_io():
    """可能会阻塞事件循环主线程的I/O函数，通常建议使用线程池来执行"""
    with open('\\dev\\urandom', 'rb') as fin:
        return f.read(100)

def cpu_bound():
    """可能会阻塞事件循环的CPU密集型函数，通常建议使用进程池来执行"""
    return sum(i*i for i in range(10**7))

async def main():
    """一级被调协程"""
    loop=asyncio.get_running_loop()
    
    #选项1：使用事件循环自动创建的executor（线程池还是进程池未知）
    result=await loop.run_in_executor(None, blocking_io)
    print('default thread pool', result)

    #选项2：使用自定义的线程池
    with concurrent.futures.ThreadPoolExecutor() as executor:
        result=await loop.run_in_executor(executor, blocking_io)
        print('custom thread pool', result)

    #选项3：使用自定义的进程池
    with concurrent.futures.ProcessPoolExecutor() as executor:
        result=await loop.run_in_executor(executor, cpu_bound)
        print('custon process pool', result)

asyncio.run(main()) #最外层的调用方——事件循环

