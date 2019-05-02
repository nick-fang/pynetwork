from multiprocessing import Process, JoinableQueue
import time

def washer(queue):
    """洗盘子的子进程"""
    for dish in ['salad', 'bread', 'entree', 'dessert']: #共有4个任务
        print(f'washing {dish} dish')
        queue.put(dish) #把洗完的盘子存进任务队列中
        time.sleep(1)

def dryer(queue):
    """烘盘子的子进程"""
    while True:
        dish = queue.get() #从任务队列中取出洗过的盘子
        print(f'drying {dish} dish')
        time.sleep(2) #烘盘子比洗盘子更费时
        queue.task_done() #每烘干一个盘子，通知队列一项任务被完成

if __name__ == '__main__':
    queue = JoinableQueue() #创建一个队列，用来保存任务进度
    washer_proc = Process(target=washer, args=(queue,)) #洗盘子，是4个任务的第一阶段
    dryer_proc = Process(target=dryer, args=(queue,)) #烘盘子，是4个任务的第二阶段
    washer_proc.start() #开始洗盘子
    dryer_proc.start() #开始烘盘子
    washer_proc.join() #在洗盘子子进程结束前，阻塞主进程
    queue.join() #在队列中的所有任务都被完成前，阻塞主进程
    dryer_proc.terminate() #烘盘子子进程是个死循环，只能强制终止
    print('All done.')
