import os
from multiprocessing import Process

def f1(arg):
    print(f'i am a process, my name is {arg} and i am running!')

if __name__=='__main__':
    print(f'i am the main process of the following process! my id is {os.getpid()}')
    #创建一个进程对象proc，target参数应传入函数名，args要求是一个元组，用于传入函数的参数，其后还有可选参数**kwargs
    proc=Process(target=f1, args=('child', ))
    #开始运行子进程
    proc.start()
    #主进程等待子进程结束
    proc.join() #如果注释掉这句，则进程结束的语句不会等到最后才打印
    print('process is end.')
