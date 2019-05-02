from concurrent import futures
import time
from flags import save_flag, get_flag, show

POP20_CC='CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR'.split()
MAX_WORKERS=20

def download_one(cc):
    """将串行版本中下载单张图像的代码剥离出来"""
    image=get_flag(cc)
    show(cc)
    save_flag(image, cc.lower()+'.gif')
    return cc

def download_many(cc_list):
    """并发执行多个下载任务"""
    cc_list=cc_list[:5] #这次演示只使用人口最多的5个国家
    with futures.ThreadPoolExecutor(max_workers=3) as executor:
        to_do=[]
        for cc in sorted(cc_list):
            future=executor.submit(download_one, cc)
            to_do.append(future)
            print('scheduled for {}: {}'.format(cc, future))
        results=[]
        for future in futures.as_completed(to_do):
            res=future.result()
            print('{} result: {!r}'.format(future, res))
            results.append(res)
    return len(results)

def main():
    """main函数记录并报告整个下载任务的耗时"""
    t0=time.time()
    count=download_many(POP20_CC)
    elapsed=time.time()-t0
    print('\n{} flags downloaded in {:.2f}s'.format(count, elapsed))

if __name__ == "__main__":
    main()
