from multiprocessing import Process, Pipe

def func(conn):
    """用于向主进程发送消息"""
    conn.send([42, None, 'hello']) #发送端，发送一个列表
    conn.close()

if __name__ == "__main__":
    PARENT_CONN, CHILD_CONN = Pipe() #管道的接收端和发送端
    proc = Process(target=func, args=(CHILD_CONN,)) #把发送端传进子进程要执行的函数中
    proc.start()
    print(PARENT_CONN.recv()) #接收端，接收到一个列表
    proc.join()
