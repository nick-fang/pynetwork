"""代码清单10-1 以WSGI应用程序形式编写的简单HTTP服务"""
from pprint import pformat
from wsgiref.simple_server import make_server

def application(environ, start_response):
    """environ是个包含请求头中所有信息的字典，start_response()是个负责发送响应头信息的函数"""
    headers = {'Content-Type':'text/plain; charset=utf-8'}
    start_response('200 OK', list(headers.items())) #第二参数是个二元元组组成的列表，发送响应头
    yield 'Here is the WSGI environment:\r\n\r\n'.encode('utf-8') #响应体会显示在浏览器中
    yield pformat(environ).encode('utf-8') #漂亮打印后的environ字典；响应体会显示在浏览器中

if __name__ == "__main__":
    httpd = make_server('127.0.0.1', 8080, application) #创建一个监听在('127.0.0.1', 8080)上的wsgi server，该server通过调用预先定义的application()函数，处理接收到的http请求，并返回待发送的http响应
    host, port = httpd.socket.getsockname()
    print('Serving on', host, 'port', port)
    httpd.serve_forever() #启动该wsgi server
