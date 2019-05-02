from concurrent import futures
import time
from random import randint
from pprint import pprint
from collections import namedtuple, OrderedDict

def return_after_5secs(num):
    """用于测试future对象的状态"""
    time.sleep(randint(1, 5))
    return f'return of (num)'

with futures.ThreadPoolExecutor(max_workers=5) as pool:
    fut_list = [pool.submit(return_after_5secs, i) for i in range(5)]

    first_com = futures.wait(fut_list, return_when='FIRST_COMPLETED')
    #将池中的future对象分组成【完成】和【未完成】，当第一条线程完成时
    print('first_completed:')
    pprint(dict(first_com._asdict())) #具名元组->有序字典->字典，漂亮打印

    all_com = futures.wait(fut_list)
    #将池中的future对象分组成【完成】和【未完成】，当所有线程完成时
    print('all_completed:')
    pprint(dict(all_com._asdict())) #具名元组->有序字典->字典，漂亮打印
