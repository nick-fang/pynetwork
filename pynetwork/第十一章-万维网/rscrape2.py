"""代码清单11-14 使用selenium递归抓取网站：爬取目标网站中的所有【站内链接】url"""
import argparse
from urllib.parse import urljoin, urlsplit
#from urllib.parse import urljoin
#from rscrape1 import main
from selenium import webdriver

class WebdriverVisitor:
    def __init__(self):
        self.browser = webdriver.Firefox()

    def parse(self):
        """是个生成器函数，依次产出页面上直接可见的绝对url"""
        url = self.browser.current_url
        links = self.browser.find_elements_by_xpath('.//a[@href]')
        for link in links:
            yield self.GET, urljoin(url, link.get_attribute('href'))

    def submit_form(self, url):
        """是个生成器函数，依次产出页面上点击【表单按钮】后才可见的绝对url"""
        import time
        self.browser.get(url)
        self.browser.find_element_by_xpath('.//form').submit()
        time.sleep(1) #等待点击表单按钮后的页面刷新
        yield from self.parse() #从parse()生成器的产出序列中产出值，相当于调用了parse函数的代码

    def GET(self, url):
        import time
        """是个生成器函数，负责爬取页面中的所有绝对url的主逻辑"""
        self.browser.get(url) #用火狐打开url指向的页面
        time.sleep(1) #等待JS脚本运行完毕
        yield from self.parse() #从parse()生成器的产出序列中产出值，相当于调用了parse函数的代码
        if self.browser.find_elements_by_xpath('.//form'):
            yield self.submit_form, url #产出(函数名, 绝对url)的二元元组？？

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
    main(WebdriverVisitor().GET)
