"""代码清单10-4 使用Werkzeug编写的WSGI可调用对象返回当前时间"""
import time
from werkzeug.wrappers import Request, Response
from wsgiref.simple_server import make_server

@Request.application
def app(request): #参数不是标准的environ和start_response
    host = request.host
    if ':' in host:
        host, port = host.split(':', 1)
    if request.method != 'GET':
        return Response('501 Not Implemented', status=501) #响应体和响应头的状态行合二为一，响应头的其余字段由模块自动生成
    elif host != '127.0.0.1' or request.path != '/':
        return Response('404 Not Found', status=404)
    else:
        return Response(time.ctime())
        
if __name__ == "__main__":
    httpd = make_server('127.0.0.1', 8000, app) #web服务器程序，调用WSGI App；后者的environ、start_response参数由web服务器提供，web服务器程序需要返回给客户端的响应，由后者处理并产出
    print('serving on', repr(httpd.socket.getsockname()))
    httpd.serve_forever()


#def decorator(app):
#    """假想的Request.application装饰器"""
#    def wrapped(environ, start_response):
#        request=foo(environ) #将environ转换成原始app()函数可以处理的request
#        response=app(request)
#        start_response(status_map[response.status], headers_dict) #从原始app()函数返回的response中提取出响应头信息，并使用start_response()发送   
#        result=response.body #从response中提取出响应体
#        return [result.encode('utf-8')] #返回响应体字节串组成的列表
#    return wrapped

#app=decorator(app) #因为web框架的用户并不会直接调用app()，所以该装饰器可以直接改变app()的调用方式？？
