"""深入理解python异步编程-异步非阻塞-select回调"""
import socket
import time
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ

sel = DefaultSelector()
keep_running = True
#路径列表跟example.com域名，能够组合出10个URL
urls_todo = {'/', '/1', '/2', '/3', '/4', '/5', '/6', '/7', '/8', '/9'}

class Crawler:
    """一个自定义的爬虫类"""
    def __init__(self, url):
        self.url = url
        self.sock = None
        self.response = b''

    def fetch(self):
        """请求连接，并向选择器注册连接套接字，监视其写就绪状态"""
        self.sock = socket.socket()
        self.sock.setblocking(False) #将该套接字设置为非阻塞模式
        try:
            self.sock.connect(('example.com', 80))
        except BlockingIOError:
            pass
        sel.register(self.sock, EVENT_WRITE, self.connected)

    def connected(self, key, mask):
        """由选择器的监视循环调用，向服务器端发送数据包，并向选择器注册连接套接字，监视其读就绪状态"""
        sel.unregister(key.fileobj) #从选择器中注销该套接字，此后监视循环将不再监视该套接字的【写就绪状态】
        get = 'GET {} HTTP/1.0\r\nHost: example.com\r\n\r\n'.format(self.url) #组织一个HTTP的GET请求
        self.sock.send(get.encode('ascii')) #向该Crawler对象的URL发起一个GET请求
        sel.register(key.fileobj, EVENT_READ, self.read_response) #重新向选择器注册该套接字，这次打算监视其【读就绪状态】

    def read_response(self, key, mask):
        """由选择器的监视循环调用，接收服务器端返回的数据包，并在所有任务结束后，终止选择器的监视循环"""
        global keep_running
        chunk = self.sock.recv(4096) #尝试接收4096字节的数据
        if chunk:
            self.response += chunk
        else: #接收到空字节串，说明服务器端关闭了连接套接字
            sel.unregister(key.fileobj) #从选择器中注销该套接字
            print(f'task {self.url}: completed.')
            urls_todo.remove(self.url) #从全局的url列表中移除该Crawler对象使用的url
        if not urls_todo: #10个URL都处理完毕后，修改全局变量stopped，终止选择器的监视循环
            keep_running = False

def loop():
    """选择器的监视循环"""
    while keep_running:
        events = sel.select(timeout=None) #是一个阻塞调用，在监视的20个读/写就绪事件中的任意一个发生前，会一直等待
        for key, mask in events:
            callback = key.data #从selectorkey中取出待回调的函数名
            callback(key, mask) #调用回调函数

if __name__ == "__main__":
    start = time.time()
    for url in urls_todo: #使用相对路径列表，实例化10个Crawler对象
        crawler = Crawler(url) #每个实例对象都拥有自己的局部变量：url、sock、response等
        crawler.fetch() #创建10个连接套接字，分别向example.com网站的10个url发起连接请求，然后分别向选择器注册这10个套接字
    loop() #启动选择器的监视循环
    end = time.time()
    print('consumed {:.2f} secs'.format(end - start))
