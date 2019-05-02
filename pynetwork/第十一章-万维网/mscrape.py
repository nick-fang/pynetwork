"""代码清单11-12 登录flask制作的账单系统app，并计算收入"""
import argparse
from urllib.parse import urljoin
import requests
import bs4
import lxml.html
from selenium import webdriver

ROW = '{:>12}  {}'

def download_page_with_requests(base):
    session = requests.Session()
    response = session.post(urljoin(base, '/login'),
                            {'username':'brandon', 'password':'atigdng'})
    assert response.url == urljoin(base, '/')
    return response.text

def download_page_with_selenium(base):
    import time
    browser = webdriver.Firefox()
    browser.get(base)
    assert browser.current_url == urljoin(base, '/login')
    usr_elem=browser.find_element_by_css_selector('input[name="username"]')
    usr_elem.send_keys('brandon') #输入用户名
    pwd_elem=browser.find_element_by_css_selector('input[name="password"]')
    pwd_elem.send_keys('atigdng') #输入密码
    pwd_elem.submit() #提交输入的内容
    time.sleep(1) #提交后，需要等待浏览器页面重定向到主页后，browser对象才会变更为主页，否则browser.current_url的值会是登录页；为什么要等待？？
    assert browser.current_url == urljoin(base, '/')
    return browser.page_source

def scrape_with_soup(text):
    """使用bs4解析抓取到的主页html文本"""
    soup = bs4.BeautifulSoup(text, 'lxml') #来自lxml库的lxml解析器比起标准库自带的html.parser更快
    total = 0
    for li in soup.find_all('li', {'class':'to'}): #待选择的标签对象，名为'li'，class属性的值为'to'
        dollars = int(li.get_text().split()[0].lstrip('$')) #把li标签的非属性字符串按空白拆分成多个子串，第一个带有'$'前缀的子串就是借出去的金额
        memo = li.find('i').get_text() #在li标签下选择名为i的子标签，后者的非属性字符串就是银行备注
        total += dollars
        print(ROW.format(dollars, memo)) #打印该帐户所有的借出条目
    print(ROW.format('-' * 8, '-' * 30)) #分隔线
    print(ROW.format(total, 'total payments made')) #打印该帐户的借出总金额

def scrape_with_lxml(text):
    """使用lxml解析抓取到的主页html文本"""
    root = lxml.html.document_fromstring(text) #解析抓取的html文本，返回root标签，类似bs4库的bs4.BeautifulSoup()函数
    total = 0
    for li in root.cssselect('li.to'): #选择class属性为'to'的li标签；cssselect()方法返回一个列表，类似bs4库的tag.findall()方法
        dollars = int(li.text_content().split()[0].lstrip('$')) #text_content()方法类似bs4库的tag.get_text()方法
        memo = li.cssselect('i')[0].text_content() #在li标签下选择名为i的子标签
        total += dollars
        print(ROW.format(dollars, memo))
    print(ROW.format('-' * 8, '-' * 30))
    print(ROW.format(total, 'total payments made'))

def main():
    parser = argparse.ArgumentParser(description='scrape our payments site.')
    parser.add_argument('url', help='the URL at which to begin')
    parser.add_argument('-l', action='store_true', help='scrape using lxml')
    parser.add_argument('-s', action='store_true', help='get with selenium')
    args = parser.parse_args()
    if args.s:
        text = download_page_with_selenium(args.url)
    else:
        text = download_page_with_requests(args.url)
    if args.l:
        scrape_with_lxml(text)
    else:
        scrape_with_soup(text)

if __name__ == "__main__":
    main()
