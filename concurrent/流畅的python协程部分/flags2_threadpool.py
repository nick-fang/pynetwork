"""《流畅的python中的示例：17-14》"""
import collections
from concurrent import futures
import requests
from tqdm import tqdm
from flags2_common import main, HTTPStatus
from flags2_sequential import download_one

DEFAULT_CONCUR_REQ = 30
MAX_CONCUR_REQ = 1000

def download_many(cc_list, base_url, verbose, concur_req):
    """使用线程池，执行下载任务"""
    counter = collections.Counter()
    with futures.ThreadPoolExecutor(max_workers=concur_req) as executor:
        to_do_map = {} #空字典，用来保存submit方法返回的future对象，future对象为键，对应的国家代码为值
        for cc in sorted(cc_list):
            future = executor.submit(download_one, cc, base_url, verbose)
            to_do_map[future] = cc
        done_iter = futures.as_completed(to_do_map)
        if not verbose:
            done_iter = tqdm(done_iter, total=len(cc_list))
        for future in done_iter:
            try:
                res = future.result()
            except requests.exceptions.HTTPError as exc:
                error_msg = 'HTTP {} - {}'.format(exc.response.status_code, exc.response.reason)
            except requests.exceptions.ConnectionError as exc:
                error_msg = 'Connection error'
            else:
                error_msg = ''
                status = res.status

            if error_msg:
                status = HTTPStatus.error
            counter[status] += 1
            if verbose and error_msg:
                cc = to_do_map[future]
                print('*** error for {}: {}'.format(cc, error_msg))
    return counter

if __name__ == "__main__":
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
