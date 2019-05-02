"""代码清单7-4 多线程服务器"""
from threading import Thread
import zen_utils

def start_threads(listener, workers=4):
    """启动4条子线程，每条子线程都使用同样的listener监听套接字，接收客户端的请求，并创建连接套接字"""
    args = (listener,) #监听套接字只有1个
    for i in range(workers): #但是服务器端创建的连接套接字有4个
        Thread(target=zen_utils.accept_connections_forever, args=args).start()

if __name__ == "__main__":
    address = zen_utils.parse_command_line('multi-threaded server')
    listener = zen_utils.create_srv_socket(address)
    start_threads(listener)
