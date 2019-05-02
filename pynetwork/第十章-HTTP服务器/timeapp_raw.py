"""代码清单10-2 用于返回当前时间的原始WSGI可调用对象"""
import time
from wsgiref.simple_server import make_server

def app(environ, start_response):
    host = environ.get('HTTP_HOST', '127.0.0.1')
    path = environ.get('PATH_INFO', '/')
    if ':' in host: #如果域名中指定了端口号
        host, port = host.split(':', 1)
    if '?' in path: #如果请求路径末尾指定了【查询参数】
        path, query = path.split('?', 1)
    headers = [('Content-Type', 'text/plain; charset=utf-8')]
    if environ['REQUEST_METHOD'] != 'GET': #如果请求方法不是GET，就返回错误页面
        start_response('501 Not Implemented', headers) #参数分别是响应头的状态码和其余字段
        yield b'501 Not Implemented'
    elif host != '127.0.0.1' or path != '/': #如果请求URL不是【127.0.0.1:8000/】，就返回错误页面
        start_response('404 Not Found', headers)
        yield b'404 Not Found'
    else:
        start_response('200 OK', headers) #参数是响应头
        yield time.ctime().encode('ascii') #产出响应体
        
if __name__ == "__main__":
    httpd = make_server('127.0.0.1', 8000, app) #web服务器程序，调用WSGI App；后者的environ、start_response参数由web服务器提供，web服务器程序需要返回给客户端的响应，由后者处理并产出
    print('serving on', repr(httpd.socket.getsockname()))
    httpd.serve_forever()
