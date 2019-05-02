import os
import time
import sys
import requests

POP20_CC='CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR'.split()
BASE_URL='http://flupy.org/data/flags'
DEST_DIR='downloads\\' #windows系统路径需要使用反斜杠

def save_flag(img, filename):
    """保存下载的图像"""
    path=os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as fp: #open函数不会帮忙新建路径中的目录，downloads目录需要自己手动建
        fp.write(img)

def get_flag(cc):
    """下载目标url指向的图像内容"""
    url='{}/{}/{}.gif'.format(BASE_URL, cc.lower(), cc.lower())
    resp=requests.get(url)
    return resp.content

def show(text):
    """每打印一个text就强制刷新shell窗口，而非默认的行缓冲刷新"""
    print(text, end=' ')
    sys.stdout.flush()

def download_many(cc_list):
    """整个下载任务的主程序，返回成功下载到的国旗数量"""
    for cc in sorted(cc_list):
        image=get_flag(cc)
        show(cc)
        save_flag(image, cc.lower()+'.gif')
    return len(cc_list)

def main(download_many):
    """main函数记录并报告整个下载任务的耗时"""
    t0=time.time()
    count=download_many(POP20_CC)
    elapsed=time.time()-t0
    print('\n{} flags downloaded in {:.2f}s'.format(count, elapsed))

if __name__ == "__main__":
    main()

