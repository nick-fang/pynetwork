"""awaitable对象与iterable对象的异与同"""
import inspect

class Foo:
    """一个可迭代对象的类"""
    def __init__(self, seq):
        self.seq = seq
    def __iter__(self):
        for i in self.seq:
            yield i
        return 'I am return value of the iterable.'

my_iter = Foo([2,3,3]) #构造一个可迭代对象
inspect.isawaitable(my_iter)
for i in my_iter:
    print(i, end=' ')

spam = iter(my_iter) #手动通过可迭代对象构造迭代器，即for...in循环内部隐式执行的代码
while True:
    try:
        next(spam)
    except StopIteration: #手动处理next()引发的【终止迭代】异常
        break




import inspect

class Bar:
    """一个可等待对象的类"""
    def __init__(self, seq):
        self.seq = seq
    def __await__(self):
        for i in self.seq:
            yield i
        return 'I am return value of the awaitable.'

async def coro(my_await):
    """await关键字只能位于协程函数中，所以我们需要通过驱动【该协程函数返回的协程对象】，来观察可等待对象是如何被await驱动的"""
    result = await my_await #await不仅可以把右侧对象的产出/yield值传回给外层的调用方，还能自动捕获右侧对象触发并向上冒泡的【终止迭代】异常，并把右侧生成器对象的返回值，赋值给其左侧的变量
    print(result)

my_await = Bar([2,3,3]) #构造一个可等待对象
inspect.isawaitable(my_await)
spam = coro(my_await) #构造一个协程对象
while True:
    try:
        spam.send(None) #驱动该协程对象，从而连锁驱动协程对象中的【await调用链】
    except StopIteration: #手动处理.send(None)引发的【终止迭代】异常
        break #既然终止迭代了，说明my_await对象中再无东西可“等”，于是退出循环
