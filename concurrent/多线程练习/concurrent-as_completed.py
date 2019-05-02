from concurrent import futures
import time
from random import randint

def return_after_5secs(num):
    """用于测试future对象的状态"""
    time.sleep(randint(1, 5)) #每个future对象封装的线程，随机休眠1-5秒
    return f'return of {num}'

with futures.ThreadPoolExecutor(max_workers=5) as pool:
    fut_list = [pool.submit(return_after_5secs, i) for i in range(5)]
    for future in futures.as_completed(fut_list):
    #as_completed函数按照future中的任务的完成先后顺序，返回future对象
    #executor.map方法则是按照参数顺序，返回future对象
        print(future.result(), future)
