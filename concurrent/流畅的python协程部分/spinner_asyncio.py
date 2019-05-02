"""《流畅的python》中的示例18-2"""
import asyncio
import itertools
import sys

async def spin(msg):
    """二级被调协程"""
    write, flush = sys.stdout.write, sys.stdout.flush #为标准输出的2个函数创建别名
    for char in itertools.cycle('|/-\\'): #这是一个无限循环
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        try:
            await asyncio.sleep(0.1) #每次循环等待/中断0.1秒时，控制权都会通过【await调用链】传回最外层的事件循环，事件循环获得控制权，才能继续轮转，异步执行其它的task对象
        except asyncio.CancelledError: #捕获supervisor()中cancel函数抛进来的【取消错误】异常
            break #退出循环，致使该协程执行完毕
        write(' ' * len(status) + '\x08' * len(status))

async def slow_function():
    """二级被调协程，假装等待I/O一段时间"""
    await asyncio.sleep(3) #跟spin()中的sleep一样，异步版的sleep()能够将控制权传回最外层，从而不阻塞事件循环的轮转
    return 42 #该协程对象的返回值，会被supervisor()中的result变量所接收

async def supervisor():
    """一级被调协程，用来调用二级被调协程"""
    spinner = asyncio.create_task(spin('thinking!')) #构建一个task对象，它会自动加入到当前的事件循环，并被后者驱动；至此，事件循环中共有2个task：1个封装自supervisor()协程，另1个封装自spin()协程，因此，这两个task才可以在事件循环中异步执行
    print('spinner object:', spinner)
    result = await slow_function() #await表达式返回协程对象的返回/return值（而非产出/yield值）
    spinner.cancel() #手动取消封住了spin()协程的task，因为后者内部是个无限循环
    return result

def main():
    """事件循环所在的主程序，即【await调用链】的最外层，用来调用一级被调协程"""
    result = asyncio.run(supervisor()) #该函数不仅创建事件循环，而且还会将传进来的协程自动封装成task对象，并加入到该事件循环中；最后，该函数的返回值，就是作为参数的协程的返回值
    print('answer:', result)

if __name__ == "__main__":
    main()
