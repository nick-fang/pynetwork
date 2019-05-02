"""使用生产者-消费者模式进行多线程编程"""
import queue
import time
import threading

class Producer(threading.Thread): #继承Thread类
    """生产者类"""
    def __init__(self, que, name):
        super().__init__(name=name) #将name值传递给Thread类的name参数
        self.que = que
    def run(self):
        for i in ['task1', 'task2', 'task3']: #共有3个任务
            self.que.put(f'{i}({self.name})') #向队列中存进一个字符串
            print(f'{self.name} put {i} into queue')
            time.sleep(1)
        print(f'{self.name} finished.')

class Consumer(threading.Thread): #继承Thread类
    """消费者类"""
    def __init__(self, que, name):
        super().__init__(name=name) #将name值传递给Thread类的name参数
        self.que = que
    def run(self):
        while True:
            value = self.que.get() #从队列中弹出一个字符串
            print(f'{self.name} get {value} from queue')
            print(f'there still exist {self.que.qsize()} tasks in the queue.')
            time.sleep(1)
            que.task_done() #que.join()的统计依据

if __name__ == "__main__":
    que = queue.Queue(3) #创建1个队列，最大可存储3个任务；2个生产者线程，每周期共生产2个任务；1个消费者线程，每周期消费1个任务；生产快过消费
    prod1 = Producer(que, 'producer1')
    prod2 = Producer(que, 'producer2')
    cons1 = Consumer(que, 'consumer1')
    prod1.start()
    prod2.start()
    cons1.daemon = True #消费者线程是个死循环，设置为守护线程后，他才能随主线程正常退出
    cons1.start()
    prod1.join() #确保2条生产者线程生产完毕
    prod2.join() #确保2条生产者线程生产完毕
    que.join() #确保所有任务处理完毕，队列为空
    print('All threads finished.')
