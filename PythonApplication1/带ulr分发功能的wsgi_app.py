"""实现了url分发功能的wsgi app()函数的调度器"""
import time
import cgi

class PathDispatcher: #因为涉及状态的保存，将调度器设计为自定义类更方便
    def __init__(self):
        self.pathmap = {} #URL映射表，将【请求方法+路径】映射到相应的wsgi app函数上

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        params = cgi.FieldStorage(environ['wsgi.input'], environ=environ) #解析URL中的查询字符串
        method = environ['REQUEST_METHOD'].lower()
        environ['params'] = {key:params.getvalue(key) for key in params} #将解析出来的查询字符串再存进environ字典中
        handler = self.pathmap.get((method, path), notfound_404) #如果找不到该请求方法+路径对应的app函数，则返回404的app函数
        return handler(environ, start_response)

    def register(self, method, path, function): #该方法可以作为注册装饰器使用？？
        self.pathmap[method.lower(), path] = function #字典的键是个元组
        return function

#html字符串，其中包含了2个格式化字符串的占位符{}
_hello_resp = """\
<html>
  <head>
    <title>Hello {name}</title>
  </head>
  <body>
    <h1>Hello {name}!</h1>
  </body>
</html>"""

_localtime_resp = """\
<?xml version="1.0"?>
<time>
  <year>{t.tm_year}</year>
  <month>{t.tm_mon}</month>
  <day>{t.tm_mday}</day>
  <hour>{t.tm_hour}</hour>
  <minute>{t.tm_min}</minute>
  <second>{t.tm_sec}</second>
</time>"""

def notfound_404(enviorn, start_response):
    """app()函数1"""
    start_response('404 Not Found', [('Content-type', 'text/plain')])
    return [b'Not Found']

def hello_world(environ, start_response):
    """app()函数2"""
    start_response('200 OK', [('Content-type', 'text/html')])
    params = environ['params']
    resp = _hello_resp.format(name=params.get('name'))
    yield resp.encode('utf-8')

def localtime(environ, start_response):
    """app()函数3"""
    start_response('200 OK', [('Content-type', 'application/xml')])
    resp = _localtime_resp.format(t=time.localtime())
    yield resp.encode('utf-8')

if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    dispatcher = PathDispatcher() #创建调度器
    dispatcher.register('GET', '/hello', hello_world) #向调度器注册app函数
    dispatcher.register('GET', '/localtime', localtime)

    httpd = make_server('', 8080, dispatcher) #创建一个web服务器
    print('serving on port 8080...')
    httpd.serve_forever()

#该服务器的测试代码
#from urllib.request import urlopen
#u=urlopen('http://localhost:8080/hello?name=Guido')
#print(u.read().decode('utf-8'))
#u=urlopen('http://localhost:8080/localtime')
#print(u.read().decode('utf-8'))



from flask import Flask
app=Flask(__name__)

@app.route('/') #装饰器应该具备的功能：1、{url:view函数}键值对的注册功能；2、接受environ、start_response参数的功能；3、内部调用start_response()发送响应头；4返回响应体字节串组成的可迭代对象；
def hello_world():
    return 'hello world!' #返回响应体的字符串；装饰器需要将其编码为字节串，然后包装成可迭代对象

if __name__=="__main__":
    app.run() #run()应该是个统一的调度器





"""flask框架的app.route()可能的机理"""
path_map={}
def register(path, methods=['GET']):
    def decorator(func):
        for method in methods:
            path_map[(method, path)]=func
        return func
    return decorator

@register('/', methods=['GET'])
def index():
    pass

@register('login', methods=['GET', 'POST'])
def login():
    pass
