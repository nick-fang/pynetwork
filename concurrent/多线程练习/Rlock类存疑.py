import threading
import time
import random

def step1():
    global result
    if lock.acquire():
        result.append('step1')
        time.sleep(2)
        lock.release()

def step2():
    global result
    if lock.acquire():
        result.append('step2')
        time.sleep(2)
        lock.release()

def showresult():
    if lock.acquire():
        step1()
        step2()
        lock.release()
    print(result)

def clearresult():
    global result
    if lock.acquire():
        result.clear()
        time.sleep(2)
        lock.release()
    print(result)

result=[]
lock=threading.RLock()
t1=threading.Thread(target=showresult)
t2=threading.Thread(target=clearresult)
t1.start()
t2.start()
