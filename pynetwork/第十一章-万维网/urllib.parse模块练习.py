"""urllib.parse模块练习"""
from urllib import parse

u = parse.urlsplit('https://www.google.com:443/search?q=apod@btnI=yes')
u #是个具名元组
u._fields #具名元组的全部字段
u.scheme #协议名
u.netloc #主机名+端口号
u.hostname #主机名
u.port #端口号
u.path #路径
u.query #查询字符串
u.fragment #片段


from urllib import parse
parse.urlunsplit(('https', 'www.google.com:443', '/search', 'q=apod@btnI=yes', ''))
parse.quote('http://example.com/Q&A/TCP+IP') #协议部分的冒号也被转义，这不是我们想要的
path = parse.quote('/Q&A/TCP+IP') #应该单独转义路径部分，然后再用urlunsplit()函数拼合成完整的URL
path
parse.urlunsplit(('http', 'example.com', path, '', ''))
parse.unquote('http://example.com/Q%26A/TCP%2BIP')

url_str = parse.quote('汉字')
url_str
parse.unquote(url_str)

u = parse.urlsplit('https://example.com/Q%26A/TCP%2FIP?q=packet+loss')
u
parse.parse_qs(u.query) #直接解析具名元组的query属性
parse.parse_qs('q=packet%20loss') #%xx转义符也能被解析
query = {'name': 'nick', 'age': 19}
parse.urlencode(query)


from urllib import parse
base = 'http://tools.ietf.org/html/rfc3986'
parse.urljoin(base, '.') #当前目录
parse.urljoin(base, '..') #上级目录
parse.urljoin(base, 'rfc7320') #url参数是个相对路径
parse.urljoin(base, '/dailydose/') #url参数是个绝对路径，则直接覆盖base参数的路径部分
parse.urljoin(base, '?version=1.0') #url参数是个查询字符串
parse.urljoin(base, '#section-5.4') #url参数是个片段

parse.urljoin(base='http://tools.ietf.org/html/rfc3986/', url='.') #目录型基地址
parse.urljoin(base='http://tools.ietf.org/html/rfc3986', url='.') #文件型基地址
parse.urljoin(base='http://tools.ietf.org/html/rfc3986/', url='rfc7320') #目录型基地址
parse.urljoin(base='http://tools.ietf.org/html/rfc3986', url='rfc7320') #文件型基地址


