"""代码清单8-1 使用Memcached为一个花销很大的操作加速"""
import memcache
import random
import time
import timeit

def compute_square(mc, n): #把缓存大字典传进需要进行复杂计算的函数
    """先在缓存大字典mc中查找输入n是否缓存过，如果没有再计算输出"""
    value = mc.get(f'square:{n}') #如果未找到，会返回None
    if value is None: #如果未在缓存中找到该输入，则进行计算
        time.sleep(0.001) #假装这是个耗时的计算
        value = n ** 2
        mc.set(f'square:{n}', value) #将{输入:输出}的键值对添加进缓存大字典
    return value #返回输出

def make_request():
    """用于timeit测试性能的辅助函数"""
    compute_square(mc, random.randint(1, 5000))

mc = memcache.Client(['127.0.0.1:11211']) #连接memcached服务器，返回的mc可以视作为一个缓存大字典
print('ten successive runs:')
for i in range(10):
    time_cost = timeit.timeit(make_request, number=2000) #运行2000次make_request()函数的耗时
    print(f'{time_cost:.2f} ', end='')
print()
