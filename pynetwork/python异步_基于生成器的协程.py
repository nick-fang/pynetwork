"""深入理解python异步编程-异步非阻塞-select协程"""
import socket
import time
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ

sel = DefaultSelector()
keep_running = True
#路径列表跟example.com域名，能够组合出10个URL
urls_todo = {'/', '/1', '/2', '/3', '/4', '/5', '/6', '/7', '/8', '/9'}

class Future:
    def __init__(self):
        self.result = None
        self._callbacks = []

    def add_done_callback(self, fn):
        self._callbacks.append(fn)

    def set_result(self, result):
        self.result = result
        for fn in self._callbacks:
            fn(self)

class Crawler:
    def __init__(self, url):
        self.url = url
        self.response = b''

    def fetch(self):
        sock = socket.socket() #已经不是self.sock了
        sock.setblocking(False)
        try:
            sock.connect(('example.com', 80))
        except BlockingIOError:
            pass
        f = Future()

        def on_connected(): #嵌套函数用来干啥？？
            f.set_result(None)

        sel.register(sock, EVENT_WRITE, on_connected)
        yield f
        sel.unregister(sock)
        get = 'GET {} HTTP/1.0\r\nHost: example.com\r\n\r\n'.format(self.url)
        sock.send(get.encode('ascii'))

        global keep_running
        while True:
            f = Future()

            def on_readable():
                f.set_result(sock.recv(4096))

            sel.register(sock, EVENT_READ, on_readable)
            chunk = yield f
            sel.unregister(sock)
            if chunk:
                self.response += chunk
            else:
                urls_todo.remove(self.url)
                if not urls_todo:
                    keep_running = False
                break

class Task:
    def __init__(self, coro):
        self.coro = coro
        f = Future()
        f.set_result(None)
        self.step(f)

    def step(self, future):
        try:
            next_future = self.coro.send(future.result)
        except StopIteration:
            return
        next_future.add_done_callback(self.step)

def loop():
    while keep_running:
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback()

if __name__ == "__main__":
    start = time.time()
    for url in urls_todo:
        crawler = Crawler(url)
        Task(crawler.fetch())
    loop()
    print(time.time() - start)





def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b'<h1>Hello, web!</h1>']

def application(environ, start_response):
    method=environ['REQUEST_METHOD']
    path=environ['PATH_INFO']
    if method=='GET' and path=='/':
        return handle_home(environ, start_response)
    if method=='POST' and path=='/singin':
        return handle_signin(environ, start_response)
    pass


