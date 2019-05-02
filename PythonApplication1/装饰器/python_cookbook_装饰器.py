
import time
from functools import wraps

def timethis(func):
    """报告函数的运行耗时"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start=time.time()
        result=func(*args, **kwargs)
        end=time.time()
        print(func.__name__, end-start)
        return result
    return wrapper

@timethis
def countdown(n:int):
    while n>0:
        n-=1



from functools import wraps

def decorator1(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('decorator 1')
        result=func(*args, **kwargs)
        return result
    return wrapper

def decorator2(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('decorator 2')
        result=func(*args, **kwargs)
        return result
    return wrapper

@decorator1
@decorator2
def add(x, y):
    return x+y



from functools import wraps
import logging

def logged(level, name=None, message=None):
    """level表示日志等级；name表示日志名，默认为被装饰函数的模块名；message表示日志内容，默认为被装饰函数的名字"""
    def decorator(func):
        logname=name if name else func.__module__
        log=logging.getLogger(logname)
        logmsg=message if message else func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            result=func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@logged(logging.DEBUG)
def add(x, y):
    return x+y

@logged(logging.CRITICAL, 'example')
def spam():
    print('spam')

@logged(logging.CRITICAL, 'example', 'this is a critical error!')
def foobar():
    print('foobar')



from functools import wraps, partial
import logging

def attach_wrapper(obj, func=None):
    if func is None:
        return partial(attach_wrapper, obj)
    setattr(obj, func.__name__, func)
    return func

def logged(level, name=None, message=None):
    def decorator(func):
        logname=name if name else func.__module__
        log=logging.getLogger(logname)
        logmsg=message if message else func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            result=func(*args, **kwargs)
            return result

        @attach_wrapper(wrapper)
        def set_level(newlevel):
            nonlocal level
            level=newlevel

        @attach_wrapper(wrapper)
        def set_message(newmsg):
            nonlocal logmsg
            logmsg=newmsg

        return wrapper
    return decorator

@logged(logging.DEBUG)
def add(x,y):
    return x+y

@logged(logging.CRITICAL, 'example')
def spam():
    print('spam!')

import logging
logging.basicConfig(level=logging.DEBUG)
add(2,3)

add.set_message('add called')
add(2,3)
add.set_level(logging.WARNING)
add(2,3)

import time
def timethis(func):
    """报告函数的运行耗时"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start=time.time()
        result=func(*args, **kwargs)
        end=time.time()
        print(func.__name__, end-start)
        return result
    return wrapper

@timethis
@logged(logging.DEBUG)
def countdown(n:int):
    while n>0:
        n-=1



from functools import wraps

class A:
    def decorator1(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print('decorator 1')
            result=func(*args, **kwargs)
            return result
        return wrapper

    @classmethod
    def decorator2(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print('decorator 2')
            result=func(*args, **kwargs)
            return result
        return wrapper

    #@A.decorator2
    #def spam(self): #装饰该类自己的方法会失败
    #    print('spam')

class Person:
    first_name=property()

    @first_name.getter
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('expected a string')
        self._first_name=value


import types
from functools import wraps

class Profiled:
    def __init__(self, func):
        wraps(func)(self)
        self.ncalls=0

    def __call__(self, *args, **kwargs):
        self.ncalls+=1
        result=self.__wrapped__(*args, **kwargs)
        return result

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)

@Profiled
def add(x, y):
    return x+y

class Spam:
    @Profiled
    def bar(self, x):
        print(self, x)



from functools import wraps
import inspect

def optional_debug(func):
    if 'debug' in inspect.getargspec(func).args: #预先检查“debug”会否与原始函数的形参名冲突
        raise TypeError('debug argument already defined')

    @wraps(func)
    def wrapper(*args, debug=False, **kwargs):
        if debug:
            print('calling', func.__name__)
        result=func(*args, **kwargs)
        return result
    return wrapper

@optional_debug
def spam(a,b,c):
    print(a,b,c)
