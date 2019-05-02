from multiprocessing import Process, Queue
import time

def write(queue):
    """向队列中写数据的子进程"""
    for value in ['a', 'b', 'c']:
        queue.put(value)
        print(f"write:\t puts '{value}' into queue and sleeps 1 sec...")
        time.sleep(1)
        print("write:\t subprocess wakeup from sleeping.")

def read(queue):
    """从队列中读数据的子进程"""
    while True:
        print("read:\t waiting write subprocess...")
        value = queue.get()
        print(f"read:\t gets '{value}' from queue.")

if __name__ == "__main__":
    queue = Queue() #主进程创建Queue，并传给各个子进程
    pwrite = Process(target=write, args=(queue,))
    pread = Process(target=read, args=(queue,))
    pwrite.start() #启动写入队列的子进程
    pread.start() #启动读取队列的子进程
    pwrite.join() #暂时阻塞主进程，等待pwrite子进程结束
    print("write:\t subprocess finishes.")
    pread.terminate() #pread子进程是个死循环，无法等待其结束，只能强行终止
    print("read:\t subprocess has been terminated.")
