"""redis消息队列练习：多个消费者"""
import os
import time
from concurrent import futures
import redis

def dryer():
    conn = redis.Redis() #redis服务器充当生产者与消费者之间的消息队列，可以运行于消费者的主机上，也可以运行于第三台主机上
    pid = os.getpid()
    print(f'dryer process {pid} is starting')
    while True:
        msg = conn.blpop('dishes', timeout=10) #从名为“dishes”的redis队列的左侧弹出一个消息元组；如果队列为空，则该方法堵塞最多20秒，然后返回None
        if not msg: #通过timeout结束消费者程序
            break
        val = msg[1].decode('utf-8') #消息元组的0号是队列名字节串，1号是消息字节串
        if val == 'quit': #通过自定义的结束信号，结束消费者程序
            break
        print(f'{pid}: dried {val}')
        time.sleep(0.1) #假装这是个耗时的工作
    print(f'dryer process {pid} is done')

if __name__=="__main__":
    with futures.ProcessPoolExecutor(max_workers=2) as executor:
        for i in range(2):
            executor.submit(dryer)
