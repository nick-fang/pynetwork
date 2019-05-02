from concurrent import futures
import urllib.request

URLS = ['http://www.bbc.co.uk', 'http://news.sohu.com', 'http://news.sina.com.cn', 'http://news.qq.com']

def load_url(url):
    with urllib.request.urlopen(url, timeout=60) as conn:
        return conn.read()

with futures.ThreadPoolExecutor(max_workers=4) as executor:
    for url, data in zip(URLS, executor.map(load_url, URLS)):
        print('{!r} page is {} bytes'.format(url, len(data)))

#跟as_completed函数不同，executor.map方法能够按照URLS列表元素的顺序，返回解析结果
#executor.map方法相比as_completed函数更简洁，但是无法单独处理个别线程中的异常？？
