"""使用多线程下载xkcd漫画"""
import os
import threading
import requests
import bs4
os.makedirs('xkcd', exist_ok=True)

def download_xkcd(start_comic, end_comic):
    """下载xkcd漫画"""
    for url_number in range(start_comic, end_comic):
        #下载网页
        print('Downloading page http://xkcd.com/{}...'.format(url_number))
        res = requests.get('http://xkcd.com/{}'.format(url_number))
        try:
            res.raise_for_status()
        except Exception as exc: #如果出现404 error，则直接进入下一个循环
            print('error: {}'.format(exc))
            continue

        #解析出漫画的url
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        comic_elem = soup.select('#comic img')
        if comic_elem == []:
            print('could not find comic image.')
        else:
            comic_url = 'http:' + comic_elem[0].get('src')
            #下载漫画图像
            print('downloading image {}...'.format(comic_url))
            res = requests.get(comic_url)
            res.raise_for_status()

            #保存漫画图像到.\\xkcd目录
            file_name = os.path.join('xkcd', os.path.basename(comic_url))
            with open(file_name, 'wb') as image_file:
                for chunk in res.iter_content(100000):
                    image_file.write(chunk)

#创建新的线程对象
dl_threads = []
for i in range(1, 501, 100): #共创建5条线程，每条负责100页
    dl_thread = threading.Thread(target=download_xkcd, args=(i, i + 99))
    dl_threads.append(dl_thread) #暂存进列表，以供后续join()
    dl_thread.start() #开始执行子线程

#等待所有的线程结束
for dl_thread in dl_threads:
    dl_thread.join()
#由主线程打印结束字样
print('done.')
