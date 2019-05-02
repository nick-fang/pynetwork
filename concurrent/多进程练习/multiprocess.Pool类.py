from multiprocessing import Pool
import os
import time
import random

def long_time_task(name):
    """打印每条进程的随机运行时间"""
    print(f'run task {name} on subprocess({os.getpid()})...')
    start = time.time()
    time.sleep(random.random() * 3) #随机休眠0~3秒
    end = time.time()
    print(f'task {name} runs {end-start:0.2f} seconds.')

if __name__ == '__main__':
    print(f'parent process {os.getpid()}.')
    proc = Pool(4) #创建一个容纳4条进程的进程池
    for i in range(5): #但是该进程池需要执行5项任务
        proc.apply_async(long_time_task, args=(i, )) #异步执行这5项任务
    print('waiting for all subprocesses done...')
    proc.close() #先关闭进程池；此时pool中的子进程未必已结束，但是池子不再接受新任务
    proc.join() #再阻塞主进程，等待进程中的子进程全部结束
    print('all subprocesses done.')
