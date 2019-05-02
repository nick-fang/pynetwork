from concurrent import futures
import time

def return_after_2secs(msg):
    """用于测试future对象的状态"""
    time.sleep(2)
    return msg

with futures.ThreadPoolExecutor(max_workers=2) as pool:
    #创建一个最大可容纳2个task的线程池
    fut_list = [pool.submit(return_after_2secs, 'hello') for i in range(4)]
    #向该线程池排进4个任务，获得4个future对象，于是只能先处理2个任务
    print('stage1:')
    for future in fut_list: #查看4个future对象的状态
        print(future.done(), repr(future))
    time.sleep(2) #等待2秒后，前2个任务已完成
    print('stage2:')
    for future in fut_list:
        print(future.done(), repr(future))
    time.sleep(2) #又等待2秒后，全部任务均已完成
    print('stage3:')
    for future in fut_list:
        print(future.done(), repr(future), future.result())
