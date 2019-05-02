HTML源码
"""
<div class="chapter course-wrap ">
  <!-- 章节标题 -->
  <h3>
    1章 ps基础知识
  </h3>
  <div class="chapter-description">
    photoshop简介、操作界面与调整、查找与编辑图像、点阵图和矢量图、光与色的基础知识、颜色混合与数字图像
  </div>
  <!-- 章节标题 end -->
  <!-- 章节小节 -->
  <ul class="video">
    <li data-media-id="2662">
      <a href='/video/2662' class="J-media-item">
        <i class="imv2-play_circle type"></i>
        1-1 photoshop简介
        (12:06)<button class="r moco-btn moco-btn-red preview-btn">开始学习</button>
      </a>
    </li>
    <li data-media-id="2664">
      <a href='/video/2664' class="J-media-item">
        <i class="imv2-play_circle type"></i>
        1-2 操作界面与调整
        (08:25)<button class="r moco-btn moco-btn-red preview-btn">开始学习</button>
      </a>
    </li>
    <li data-media-id="2665">
      <a href='/video/2665' class="J-media-item">
        <i class="imv2-play_circle type"></i>
        1-3 查找与编辑图像
"""


import requests
from bs4 import BeautifulSoup

def getHTMLCourse(url_t):
    """获取课程章节的html源码"""
    try:
        d = requests.get(url_t, timeout = 100)
        d.raise_for_status()
        d.encoding = d.apparent_encoding
        return d.text
    except:
        return ""

def getcourse(title_list, sub_title_list, html_t): #course1和course2是2个空列表
    """解析课程的标题和副标题"""
    soup = BeautifulSoup(html_t, "html.parser")
    div_tags=soup.find_all('div', {'class':"chapter course-wrap "})
    i_tags=soup.find_all('i', {'class':"imv2-play_circle type"})
    for div in div_tags:
        title_list.append(div.h3.string.strip())
    for i in i_tags:
        sub_title_list.append(list(i.parent.strings)[1][0:100].strip())

def savecourse():
    """保存课程的标题和副标题"""
    with open('course.txt', 'wt') as fout:
        fout.write("标题：\n")
        fout.writelines([i+'\n' for i in title_list])
        fout.write("副标题：\n")
        fout.writelines([i+'\n' for i in sub_title_list])

if __name__=='__main__':
    title_list=[]
    sub_title_list=[]
    url_t='https://www.imooc.com/learn/159'
    html_t= getHTMLCourse(url_t)
    getcourse(title_list, sub_title_list, html_t)
    savecourse()
