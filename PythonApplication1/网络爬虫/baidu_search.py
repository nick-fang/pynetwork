"""百度同时打开多个搜索页，cmd运行命令python baidu_search.py [关键词] 页面数量"""

import sys, requests, bs4, webbrowser

def fetch_url():
    """sys抓取命令行参数代表的搜索关键词，返回搜索页的url"""
    global num
    if len(sys.argv)>2 and sys.argv[-1].isdigit():
        num=eval(sys.argv[-1])
        keyword=" ".join(sys.argv[1:-1]) #把实参列表转换成空格间隔的字符串
        return 'http://www.baidu.com/s?wd='+keyword
    else:
        print('need last argument to be digit, and other arguments except 1st as keyword!')
        sys.exit()

def getHTMLText(url):
    """requests获取百度搜索结果页"""
    try:
        r=requests.get(url, timeout=30)
        r.raise_for_status()
    except:
        return ""
    else:
        r.encoding=r.apparent_encoding
        return r.text

def parserPage(html):
    """bs4解析r.text, 获取搜索结果链接的列表"""
    soup=bs4.BeautifulSoup(html, 'html.parser')
    a_tags=soup.select('h3[class="t"] a')
    link_list=[a_tag.attrs.get('href') for a_tag in a_tags]
    return link_list

def open_links(link_list, num):
    """webbrower循环打开列表中的链接"""
    for link in link_list[0:num]:
        webbrowser.open(link)

url=fetch_url()
html=getHTMLText(url)
link_list=parserPage(html)
open_links(link_list, num)

