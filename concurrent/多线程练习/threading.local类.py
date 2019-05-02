import threading

def task():
    """两个子线程都要执行的函数"""
    LOCAL.count = 0 #初始化一个线程内的全局变量，该变量在线程间互不影响；count相当于全局字典的第二层key，即globalDict[threading.current_thread()][count]
    for i in range(3):
        count_plus()

def count_plus():
    """被子线程执行的函数体内部代码调用到的函数"""
    LOCAL.count += 1 #无需通过形参传递，可以对该线程内的全局变量直接进行修改
    print(f"{threading.current_thread().name}'s LOCAL.count=={LOCAL.count}")

if __name__ == "__main__":
    LOCAL = threading.local() #创建一个全局的local对象，本质上相当于一个二层嵌套字典，字典的第一层key是threading.current_thread()
    t1 = threading.Thread(target=task)
    t1.start()
    t1.join()
    t2 = threading.Thread(target=task)
    t2.start()
    t2.join()
