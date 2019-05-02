"""代码清单11-13 进行GET操作的简单递归网络抓取器：爬取目标网站中的所有【站内链接】url"""
import argparse
from urllib.parse import urljoin, urlsplit
import requests
from lxml import etree

def GET(url):
    """是个生成器函数，负责绝对url的爬取工作；产出(GET函数名, 绝对url)的二元元组"""
    response = requests.get(url)
    if response.headers.get('Content-Type', '').split(';')[0] != 'text/html': #如果响应体的类型不是html，就跳出函数
        return
    text = response.text
    try:
        html = etree.HTML(text) #解析html文本，返回root标签；类似bs4.BeautifulSoup()函数
    except Exception as exc:
        print('    {}: {}'.format(exc.__class__.__name__, exc)) #exc所属的异常类，exc实例的说明字符串
        return
    links = html.findall('.//a[@href]') #抓取root标签（即整个页面）中的所有<a></a>标签
    for link in links:
        yield GET, urljoin(url, link.attrib['href']) #将抓取的每一个<a>标签中的链接地址转换成包含域名的【绝对url】，并产出

def scrape(start, domain):
    """负责维护绝对url的2个集合，打印分析结果，并调用GET爬取函数"""
    further_work = {start} #是个集合，存储尚未访问并爬取的绝对url
    already_seen = {start} #是个集合，存储已经发现的绝对url
    while further_work: #只要还有绝对url未访问过，就继续循环
        function, url, *etc = further_work.pop() #function就是本模块中的GET函数
        print(function.__name__, url, *etc) #打印待访问的绝对url
        for call_tuple in function(url, *etc): #迭代GET函数返回的生成器
            if call_tuple in already_seen: #如果GET函数抓取到的绝对url是重复的，则略过
                continue
            already_seen.add(call_tuple) #对于非重复的绝对url，将其添加进“已经发现”的集合
            function, url, *etc = call_tuple
            if urlsplit(url).netloc != domain: #如果该绝对url不是【站内链接】，则略过
                continue
            further_work.add(call_tuple) #对于站内链接的绝对url，将其添加进“尚未爬取”的集合

def main(GET):
    parser = argparse.ArgumentParser(description='scrape a simple site.')
    parser.add_argument('url', help='the URL at which to begin')
    start_url = parser.parse_args().url #取出解析好的命令行参数
    domain = urlsplit(start_url).netloc #命令行输入的url的域名部分
    scrape((GET, start_url), domain) #开始爬取

if __name__ == "__main__":
    main(GET)
