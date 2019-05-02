"""一个异步上下文管理器的实现"""

class AsyncContextor:
    """一个极简的异步上下文管理器类"""
    def __init__(self):
        self.closed = None #None表示未操作过，准备工作会将该属性改为False，而清理工作会将该属性改为True
    async def __aenter__(self):
        """进入协议，不仅执行一些准备工作，而且该方法【返回的协程对象的返回值】会被赋值给as后面的变量"""
        print('set-up work starts...')
        self.closed = False
        return self #返回【异步上下文管理器对象】自身，这是通常情况；但是我们也可以选择返回其他值
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """退出协议，执行一些清理工作；因为是异步版，所以通常会await一个负责清理工作的协程对象"""
        await self.cleanup()
    async def cleanup(self):
        """负责清理工作的协程函数"""
        self.closed = True
        print('cleanup work done.')

async def main():
    """执行异步上下文管理器"""
    ac = AsyncContextor() #实例化一个异步上下文管理器对象
    async with ac as foo:
        print('foo is:', repr(foo))
        print('if foo == ac?', foo == ac)
    print('is async contextor closed safely?', ac.closed)

try:
    main().send(None) #因为await关键字只能用于协程函数内，所以在最外层得用.send(None)来驱动main()协程对象
except StopIteration as exc: #.send(None)不像await那样能够自动处理【终止迭代】异常，所以我们需要手动处理
    result = exc.value


import sys

async def main():
    """异步上下文管理器语法的本质"""
    ac = AsyncContextor() #实例化一个异步上下文管理器对象
    foo = await ac.__aenter__() #执行准备工作，并且把__aenter__()协程的返回值赋值给foo变量
    try:
        print('foo is:', repr(foo))
        print('if foo == ac?', foo == ac)
    finally:
        await ac.__aexit__(*sys.exc_info()) #finally关键字确保，无论try子句中发生了什么（正常、异常、函数return等），清理工作都一定会被执行；sys.exc_info()的返回值拆包后，就是try子句中触发的异常的类型、实例和traceback，若无异常，则默认为3个None
    print('is async contextor closed safely?', ac.closed)

try:
    main().send(None) #因为await关键字只能用于协程函数内，所以在最外层得用.send(None)来驱动main()协程对象
except StopIteration as exc: #.send(None)不像await那样能够自动处理【终止迭代】异常，所以我们需要手动处理
    result = exc.value
