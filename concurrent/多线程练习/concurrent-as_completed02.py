from concurrent import futures
import urllib.request

URLS = ['http://news.sohu.com', 'http://news.sina.com.cn', 'http://news.qq.com']

def load_url(url):
    """conn对象类似requests库的request对象，conn.read()方法返回请求页面的字节串表示"""
    with urllib.request.urlopen(url, timeout=60) as conn:
        return conn.read()

with futures.ThreadPoolExecutor(max_workers=3) as executor: #3条线程，对应3个解析url的任务
    future_to_url = {executor.submit(load_url, url):url for url in URLS}
    #字典推导：键是future对象，值是该future对象线程解析的url
    for future in futures.as_completed(future_to_url.keys()): #3个future对象中，谁封装的线程先执行完毕，谁就先被as_completed函数返回
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('{!r} generated an exception: {}'.format(url, exc))
        else:
            print('{!r} page is {} bytes'.format(url, len(data)))

#从运行结果看，as_completed不是按照URLS列表元素的顺序返回的
