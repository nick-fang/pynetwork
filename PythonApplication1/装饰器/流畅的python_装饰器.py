
def mydecorator(function):
    def wrapped(*args, **kwargs):
        #在调用原始函数之前，做点什么
        result = function(*args, **kwargs)
        #在调用原始函数之后，做点什么
        return result #最后返回原始函数的结果
    return wrapped

class DecoratorAsClass:
    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        #在调用原始函数之前，做点什么
        result = self.function(*args, **kwargs)
        #在调用原始函数之后，做点什么
        return result #最后返回原始函数的结果

def repeat(number=3):
    """装饰器工厂函数；多次重复执行装饰函数，返回最后一次原始函数调用的值作为结果"""
    def actual_decorator(function):
        """装饰器"""
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(number):
                result = function(*args, **kwargs)
            return result
        return wrapper
    return actual_decorator #返回装饰器对象
from functools import wraps

def preserving_decorator(function):
    @wraps(function)
    def wrapped(*args, **kwargs):
        """包装函数的doc"""
        result = function(*args, **kwargs)
        return result
    return wrapped

@preserving_decorator
def function_with_important_docstring():
    """被装饰函数的原doc"""
    pass



rpc_info = {}

def xmlrpc(in_=(), out=(type(None),)):
    def _xmlrpc(function):
        #注册签名
        func_name = function.__name__
        rpc_info[func_name] = (in_, out)
        def _check_types(elements, types):
            """用来检查类型的子函数；elements是待检测的参数或返回值，types是预先设定好的待匹配类型"""
            if len(elements) != len(types):
                raise TypeError
            typed = enumerate(zip(elements, types))
            for index, couple in typed:
                arg, of_the_right_type = couple
                if isinstance(arg, of_the_right_type):
                    continue
                raise TypeError('arg {} should be {}'.format(index, of_the_right_type))
        
        def __xmlrpc(*args):
            #检查输入的内容
            checkable_args = args[1:] #去掉self
            _check_types(checkable_args, in_) #检查参数的类型
            result = function(*args)
            if not type(result) in (tuple, list):
                checkable_res = (result,)
            else:
                checkable_res = result
            _check_types(checkable_res, out) #检查返回值的类型
            return result
        return __xmlrpc
    return _xmlrpc

class RPCView:
    @xmlrpc((int, int))
    def meth1(self, int1, int2):
        print('received {} and {}'.format(int1, int2))

    @xmlrpc((str,), (int,))
    def meth2(self, phrase):
        print('received {}'.format(phrase))
        return 12



import time
import hashlib
import pickle

cache = {}

def is_obsolete(entry, duration):
    return time.time() - entry['time'] > duration

def compute_key(function, args, kw): #将参数元组哈希化后，作为缓存字典的键
    key = pickle.dumps((function.__name__, args, kw))
    return hashlib.sha1(key).hexdigest()

def memoize(duration=10):
    def _memoize(function):
        def __memoize(*args, **kwargs):
            key = compute_key(function, args, kwargs)
            if (key in cache and not is_obsolete(cache[key], duration)):
                print('we got a winner')
                return cache[key]['value']
            result = function(*args, **kwargs)
            cache[key] = {'value':result, 'time':time.time()}
            return result
        return __memoize #返回包装函数
    return _memoize #返回装饰器
@memoize(duration=1)
def very_very_very_complex_stuff(a, b):
    return a + b

very_very_very_complex_stuff(2, 2)
very_very_very_complex_stuff(2, 2)
cache
time.sleep(2)
cache
very_very_very_complex_stuff(2, 2)



class User(object):
    def __init__(self, roles):
        self.roles = roles

class Unauthorized(Exception):
    pass

def protect(role):
    def _protect(function):
        def __protect(*args, **kwargs):
            user = globals().get('user')
            if user is None or role not in user.roles:
                raise Unauthorized("i won't tell you")
            result = function(*args, **kwargs)
            return result
        return __protect #返回包装函数
    return _protect #返回装饰器对象
tarek = User(('admin', 'user'))
bill = User(('user',))
class MySecrets(object):
    @protect('admin')
    def waffle_recipe(self):
        print('use tons of butter!')
these_are = MySecrets()
user = tarek
these_are.waffle_recipe()
user = bill
these_are.waffle_recipe()



from threading import RLock

lock = RLock()
def synchronized(function):
    def _synchronized(*args, **kwargs):
        with lock:
            result = function(*args, **kwargs)
        return result
    return _synchronized

@synchronized
def thread_safe():
    pass

