"""中国大学排名定向爬虫"""

#html源代码
"""
<tr class="alt">
    <td>1</td>
    <td>
    <div align="left">
        清华大学
    </div>
    </td>
    <td>北京市</td>
    <td>95.9</td>
    <td class="hidden-xs need-hidden indicator5">100.0</td>
    <td class="hidden-xs need-hidden indicator6" style="display:none;">97.90%</td>
    <td class="hidden-xs need-hidden indicator7" style="display:none;">37342</td>
    <td class="hidden-xs need-hidden indicator8" style="display:none;">1.298</td>
    <td class="hidden-xs need-hidden indicator9" style="display:none;">1177</td>
    <td class="hidden-xs need-hidden indicator10" style="display:none;">109</td>
    <td class="hidden-xs need-hidden indicator11" style="display:none;">1137711</td>
    <td class="hidden-xs need-hidden indicator12" style="display:none;">1187</td>
    <td class="hidden-xs need-hidden indicator13" style="display:none;">593522</td>
</tr>
"""

import requests
import bs4
from bs4 import BeautifulSoup

def getHTMLText(url):
    """"获取网页的html文本"""
    try:
        r=requests.get(url,timeout=30)
        r.raise_for_status()
    except:
        return ""
    else:
        r.encoding=r.apparent_encoding
        return r.text

def fillUnivList(ulist,html):
    """从html文本中提取并保存有效信息"""
    soup=BeautifulSoup(html,"html.parser")
    for tr in soup.find('tbody').children: #迭代tbody标签下的子标签
        if isinstance(tr,bs4.element.Tag): #过滤迭代到的属性字符串，需要使用到bs4库
            tds=tr.find_all('td') #返回td标签组成的列表
            ulist.append([i.string for i in tds[0:3]]) #把tds中的0、1、2号标签的属性字符串，作为一个子列表添加到ulist中

def printUnivList(ulist,num):
    """格式化打印需要展示的内容"""
    formated_s="{0:^10}\t{1:{3}^10}\t{2:^10}"
    print(formated_s.format("排名","学校名称","省市",chr(12288))) #打印表头
    for i in range(num):
        print(formated_s.format(ulist[i][0],ulist[i][1],ulist[i][2],chr(12288)))

def main():
    url="http://www.zuihaodaxue.cn/zuihaodaxuepaiming2016.html"
    html=getHTMLText(url)
    ulist=[] #用于保存提取信息的二维列表
    fillUnivList(ulist,html)
    printUnivList(ulist,20)

main()
