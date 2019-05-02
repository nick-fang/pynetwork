from threading import Thread
import queue
import time

def washer(dish_queue):
    """洗盘子的子线程"""
    for dish in ['salad', 'bread', 'entree', 'dessert']: #共有4个任务
        print(f'washing {dish}')
        dish_queue.put(dish) #把洗完的盘子存进任务队列中
        time.sleep(1)

def dryer(dish_queue):
    """烘盘子的子线程"""
    while True:
        dish = dish_queue.get() #从任务队列中取出洗过的盘子
        print(f'drying {dish}')
        time.sleep(2) #烘盘子比洗盘子更费时
        dish_queue.task_done() #每烘干一个盘子，通知队列一项任务被完成

DISH_Q = queue.Queue() #创建一个队列，用来保存任务进度
washer_thre = Thread(target=washer, args=(DISH_Q,)) #洗盘子，是4个任务的第一阶段
washer_thre.start() #开始洗盘子
for n in range(2): #烘盘子，是4个任务的第二阶段；因为烘盘子耗时是洗盘子的2倍，为烘盘子增加线程后，能够提升整体效率
    dryer_thre = Thread(target=dryer, args=(DISH_Q,), daemon=True) #烘盘子子线程是个死循环，设置为守护线程后，能够随着主线程的结束而结束
    dryer_thre.start() #开始烘盘子
washer_thre.join() #在洗盘子子进程结束前，阻塞主进程
DISH_Q.join() #在队列中的所有任务都被完成前，阻塞主进程
print('All done.')
