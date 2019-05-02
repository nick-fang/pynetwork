import collections
import requests
from tqdm import tqdm
from flags2_common import main, save_flag, HTTPStatus, Result

DEFAULT_CONCUR_REQ = 1
MAX_CONCUR_REQ = 1

def get_flag(base_url, cc):
    url = '{}/{}/{}.gif'.format(base_url, cc.lower(), cc.lower())
    resp = requests.get(url)
    if resp.status_code != 200:
        resp.raise_for_status()
    return resp.content

def download_one(cc, base_url, verbose=False):
    try:
        image = get_flag(base_url, cc)
    except requests.exceptions.HTTPError as exc:
        res = exc.response
        if res.status_code == 404: #如果异常是404，则会被压下来，而不传到download_many函数
            status = HTTPStatus.not_found #是个枚举成员
            msg = 'not found'
        else:
            raise
    else:
        save_flag(image, cc.lower() + '.gif')
        status = HTTPStatus.ok #是个枚举成员
        msg = 'ok'

    if verbose:
        print(cc, msg)
    return Result(status, cc) #具名元组的第一字段是个枚举成员，第二字段是个国旗代码字符串

def download_many(cc_list, base_url, verbose, max_req):
    """verbose/详细参数为True，则将显示每次下载的状态或者错误信息"""
    counter = collections.Counter()
    cc_iter = sorted(cc_list)
    if not verbose: #如果verbose参数为True，则不显示进度条？？
        cc_iter = tqdm(cc_iter) #显示进度条
    for cc in cc_iter:
        try:
            res = download_one(cc, base_url, verbose)
        except requests.exceptions.HTTPError as exc:
            error_msg = 'HTTP error {} - {}'.format(exc.response.status_code, exc.response.reason)
        except requests.exceptions.ConnectionError as exc:
            error_msg = 'Connection error'
        else:
            error_msg = ''
            status = res.status #具名元组的status字段，是个枚举成员

        if error_msg: #404以外的异常，被视为error枚举成员；404异常，被视为not_found成员；正常下载，被视为ok成员
            status = HTTPStatus.error #是个枚举成员
        counter[status] += 1 #把枚举成员作为计数器的键
        if verbose and error_msg: #如果有异常，且verbose参数为True，则显示错误信息
            print('*** error for {}: {}'.format(cc, error_msg))
    return counter

if __name__ == "__main__":
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
