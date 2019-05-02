
import time
import functools

def clock(func):
    """一个会打印函数执行耗时的装饰器"""
    @functools.wraps(func)
    def wrapped(*args):
        t0 = time.time()
        result = func(*args)
        elapsed = time.time() - t0
        arg_str = ', '.join(repr(i) for i in args)
        print('[{:.8f}s] {}({}) -> {!r}'.format(elapsed, func.__name__, arg_str, result))
        return result
    return wrapped

@clock
def factorial(n):
    """计算阶乘"""
    return 1 if n < 2 else n * factorial(n - 1)

factorial(6)


import time
import functools

def clock(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        """this is decorator's doc"""
        t0 = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - t0
        arg_lst = []
        if args: #收集位置实参
            arg_lst.extend([repr(i) for i in args])
        if kwargs: #收集关键字实参
            arg_lst.extend(['{}={!r}'.format(k, w) for k, w in kwargs.items()])
        arg_str = ', '.join(arg_lst) #拼接成函数调用时的参数字符串
        print('[{:.8f}s] {}({}) -> {!r}'.format(elapsed, func.__name__, arg_str, result))
        return result
    return wrapped



#@functools.lru_cache()
#@clock
#def fibonacci(n):
#    return n if n<2 else fibonacci(n-2)+fibonacci(n-1)

#fibonacci(6)

import functools

def mydecorator(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        """this is decorator's doc"""
        result = func(*args, **kwargs)
        return result
    return wrapped

@mydecorator
def myfunc():
    """this is myfunc's doc"""
    pass

myfunc
myfunc.__name__
myfunc.__doc__


def deco1(func):
    def wrapped(*args):
        result = func(*args)
        return result
    return wrapped

def deco2(func):
    def wrapped(*args):
        result = func(*args)
        return result
    return wrapped

@deco2
@deco1
def target():
    pass
target.__qualname__


def mydeco_factory(custom):
    def mydecorator(func):
        def wrapped(*args, **kwargs):
            #在调用原始函数之前，做点使用custom参数的代码
            result = func(*args, **kwargs)
            #在调用原始函数之后，做点使用custom参数的代码
            return result #最后返回原始函数的结果
        return wrapped
    return mydecorator

@mydeco_factory(custom=233)
def myfunc():
    pass
myfunc.__qualname__
