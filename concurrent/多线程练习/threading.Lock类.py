"""子线程上锁，则串行执行；子线程不上锁，则并发执行"""

import threading
import time

number = 0
LOCK = threading.Lock()
def run():
    """上了锁的线程"""
    global number #声明全局变量
    with LOCK: #使用上下文管理器管理锁的获得和释放
        number += 1 #修改全局变量
        print(number)
        time.sleep(1)

start = time.perf_counter()
tlist = []
for i in range(3): #创建3条子线程
    t = threading.Thread(target=run)
    t.start() #并发启动子线程
    tlist.append(t)
for j in tlist:
    j.join() #每条子线程结束前，都会尝试阻塞主线程
print('done in {:.3f} secs.'.format(time.perf_counter() - start))
