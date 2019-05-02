"""
淘宝商品信息定向爬虫
目标：获取淘宝搜索页面的信息，提取其中的商品名称和价格
1、获得搜索接口
2、翻页的处理

"""
#url模式
"""
https://s.taobao.com/search?q=%E4%B9%A6%E5%8C%85&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306

https://s.taobao.com/search?q=%E4%B9%A6%E5%8C%85&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&bcoffset=3&ntoffset=3&p4ppushleft=1%2C48&s=44

https://s.taobao.com/search?q=%E4%B9%A6%E5%8C%85&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&bcoffset=0&ntoffset=6&p4ppushleft=1%2C48&s=88
"""

#单件商品的HTML源码
"""
{"p4p":1,"p4pSameHeight":true,"nid":"530894196576","category":"","pid":"","title":"瑞士军刀双肩包瑞士中学生\u003cspan class\u003dH\u003e书包\u003c/span\u003e女休闲男士商务旅行大容量电脑背包","raw_title":"瑞士军刀男士双肩背包旅行商务出差电脑书包","pic_url":"//g-search1.alicdn.com/img/bao/uploaded/i4/imgextra/i4/46076546/TB26Rh1d1LM8KJjSZFqXXa7.FXa_!!0-saturn_solar.jpg","detail_url":"https://click.simba.taobao.com/cc_im?p\u003d%CA%E9%B0%FC\u0026s\u003d1926363468\u0026k\u003d577\u0026e\u003d1tA9GG6KOsMw7pnEWpSRu8f1YbJP5H5CWrUf4AXlp8RiS6d%2FrZIXsJllLmLoN9WRprThtGFoK7XP%2BJmV4eb%2BwDmrboWs5tP1obN0tqixba7%2BJXHYRN5zVyUzZq5bbLDgv2efavuDCe%2BHUHHexL3Dew16MgQwKu91aPHaYAzxmSf4ON3jx9im72CDA95EhVXhkc%2Bvdp7lFW%2FP9a7eNE3tZL94oCgqEQBM%2Fn95eau7j7NNVyvhRBFhmY8N%2FevR8wAV7mLxhbeIk6ZGwJ3XD%2BHbVaNBJerXaxv6rVwo4el8OqZ0AjwiR3dBzJonR0nRV18b2XZpQxW%2FjQNhuxqjtZVkHMFkWH4%2FRmUFX3Bqq5XNGGRzsUS%2Bq8NoghcBVA47H7hB5UCOYZJ5BqJggiRDVR8qReBK9nmhTF6gA508lKSTLaDEIsUxUb7WfA5AkbdQbgPBoaXf%2FGN%2FhQs1R0giNbjTufF2%2BlkmDY8zUtYl6K0OHxLrhW4EhnfONJydmbpS6dNhUJLxBGyU4v%2FYy8FtLmIAqJYDIJPA9ECVKeO1%2BtkXtaO7mGoC8zv5vkTRu%2BUMDpDD","view_price":"138.00","view_fee":"0.00","item_loc":"广东 广州","view_sales":"6347人付款","comment_count":"","user_id":"1773244767","nick":"鑫运箱包专营店","shopcard":{"levelClasses":[],"isTmall":true,"delivery":[0,1,1928],"description":[0,1,2652],"service":[0,1,2048],"encryptedUserId":"UvFcuvGI0MmcLMWTT"},"icon":[{"title":"掌柜热卖宝贝","dom_class":"icon-service-remai","position":"1","show_type":"0","icon_category":"baobei","outer_text":"0","html":"","icon_key":"icon-service-remai","trace":"srpservice","traceIdx":0,"innerText":"掌柜热卖宝贝","url":"//re.taobao.com/search?keyword\u003d%CA%E9%B0%FC\u0026refpid\u003d420432_1006\u0026frcatid\u003d\u0026"},{"title":"尚天猫，就购了","dom_class":"icon-service-tianmao","position":"1","show_type":"0","icon_category":"baobei","outer_text":"0","html":"","icon_key":"icon-service-tianmao","trace":"srpservice","traceIdx":1,"innerText":"天猫宝贝"},{"title":"保险理赔","dom_class":"icon-service-baoxian","position":"99","show_type":"1","icon_category":"baobei","outer_text":"0","html":"","icon_key":"icon-service-baoxian","trace":"srpservice","traceIdx":2,"innerText":"分组-保险理赔","iconPopupComplex":{"popup_title":"保险理赔","subIcons":[{"dom_class":"icon-service-yunfeixian","icon_content":"卖家赠送退货运费险"}]}},{"title":"公益宝贝","dom_class":"icon-fest-gongyibaobei","position":"2","show_type":"0","icon_category":"baobei","outer_text":"0","html":"","icon_key":"icon-fest-gongyibaobei","trace":"srpservice","traceIdx":3,"innerText":"公益宝贝"}],"isHideIM":true,"isHideNick":false,"comment_url":"https://click.simba.taobao.com/cc_im?p\u003d%CA%E9%B0%FC\u0026s\u003d1926363468\u0026k\u003d577\u0026e\u003d1tA9GG6KOsMw7pnEWpSRu8f1YbJP5H5CWrUf4AXlp8RiS6d%2FrZIXsJllLmLoN9WRprThtGFoK7XP%2BJmV4eb%2BwDmrboWs5tP1obN0tqixba7%2BJXHYRN5zVyUzZq5bbLDgv2efavuDCe%2BHUHHexL3Dew16MgQwKu91aPHaYAzxmSf4ON3jx9im72CDA95EhVXhkc%2Bvdp7lFW%2FP9a7eNE3tZL94oCgqEQBM%2Fn95eau7j7NNVyvhRBFhmY8N%2FevR8wAV7mLxhbeIk6ZGwJ3XD%2BHbVaNBJerXaxv6rVwo4el8OqZ0AjwiR3dBzJonR0nRV18b2XZpQxW%2FjQNhuxqjtZVkHMFkWH4%2FRmUFX3Bqq5XNGGRzsUS%2Bq8NoghcBVA47H7hB5UCOYZJ5BqJggiRDVR8qReBK9nmhTF6gA508lKSTLaDEIsUxUb7WfA5AkbdQbgPBoaXf%2FGN%2FhQs1R0giNbjTufF2%2BlkmDY8zUtYl6K0OHxLrhW4EhnfONJydmbpS6dNhUJLxBGyU4v%2FYy8FtLmIAqJYDIJPA9ECVKeO1%2BtkXtaO7mGoC8zv5vkTRu%2BUMDpDD\u0026on_comment\u003d1","shopLink":"https://click.simba.taobao.com/cc_im?p\u003d%CA%E9%B0%FC\u0026s\u003d1926363468\u0026k\u003d545\u0026e\u003dhUggRTGLM34w7pnEWpSRu8f1YbJP5H5CWrUf4AXlp8RiS6d%2FrZIXsJllLmLoN9WRprThtGFoK7XoEzWPSz1rHTmrboWs5tP1obN0tqixba7%2BJXHYRN5zVyUzZq5bbLDgv2efavuDCe%2BHUHHexL3Dew16MgQwKu91aPHaYAzxmSf4ON3jx9im72CDA95EhVXhkc%2Bvdp7lFW%2FP9a7eNE3tZL94oCgqEQBM%2Fn95eau7j7NNVyvhRBFhmY8N%2FevR8wAV7mLxhbeIk6ZGwJ3XD%2BHbVaNBJerXaxv6rVwo4el8OqZ0AjwiR3dBzJonR0nRV18b2XZpQxW%2FjQNhuxqjtZVkHMFkWH4%2FRmUFX3Bqq5XNGGRzsUS%2Bq8NoghcBVA47H7hB5UCOYZJ5BqJggiRDVR8qReBK9nmhTF6gZfHvDcnC7z1j00PlyFq4AFEKhijODBKemUi%2ByVCu6BZ0AjwiR3dBzM3FfxZD5PtYIuGT2Om4jrxqgVwH4YTyxbFYS4p7zaWV8Orsu4EHkpxdWnDHofIU09g%2BcXk0x8N%2F"},{"i2iTags":{"samestyle":{"url":""},"similar":{"url":"/search?type\u003dsimilar\u0026app\u003di2i\u0026rec_type\u003d1\u0026uniqpid\u003d\u0026nid\u003d43302933537"}},
"""


import requests
import re

def getHTMLText(url):
    try:
        r=requests.get(url,timeout=30)
        r.raise_for_status()
    except:
        return ""
    else:
        r.encoding=r.apparent_encoding
        return r.text

def parserPage(info_list,html):
    try:
        price_lt=re.findall(r'"view_price":"[\d\.]*"',html)
        title_lt=re.findall(r'"raw_title":"\w*"',html) #\w能够匹配中文字符
        for i in range (len(price_lt)):
            price=eval(price_lt[i].split(':')[1]) #价格字符串拆分后的第2个元素去引号，就是代表价格的一个数值字符串，仍旧带有双引号
            title=eval(title_lt[i].split(':')[1]) #带有双引号的标题字符串
            info_list.append([price, title])
    except:
        print ("")

def printGoodsList(info_list):
    formated_s="{:4}\t{:8}\t{:16}"
    print(formated_s.format("序号","价格","商品名称"))
    count=0
    for g in info_list:
        count+=1
        print(formated_s.format(count,g[0],g[1]))

def main():
    goods='扫地机器人'
    depth=2
    start_url='https://s.taobao.com/search?q='+goods
    info_list=[]
    for i in range(depth):
        try:
            url=start_url+'&s='+str(44*i)
            html=getHTMLText(url)
            parserPage(info_list,html)
        except:
            continue
    printGoodsList(info_list)

main()


