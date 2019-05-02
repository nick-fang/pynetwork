import threading

def do_sth(event):
    """子线程要运行的函数"""
    print('事件还未发生……')
    event.wait() #子线程在这里被阻塞
    print('事件已经发生')

EVENT = threading.Event() #创建一个event对象，其内部标记默认为False
tlist = []
for i in range(3):
    t = threading.Thread(target=do_sth, args=(EVENT,))
    t.start()
    tlist.append(t)
EVENT.set() #将事件的内部标记修改为True，代表该事件发生
for t in tlist:
    t.join()
print('All done.')
