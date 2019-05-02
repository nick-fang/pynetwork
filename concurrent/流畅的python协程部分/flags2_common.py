"""为后续flag示例提供实用函数"""
import os
import time
import sys
import string
import argparse
from collections import namedtuple
from enum import Enum #从枚举模块中导入枚举类型
Result = namedtuple('Result', ['status', 'data'])
HTTPStatus = Enum('status', 'ok not_found error') #枚举模板名为status，包括3个枚举成员：ok、not_found、error
POP20_CC = 'CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR'.split() #是个包含国旗代码字符串的列表
DEFAULT_CONCUR_REQ = 1 #默认的并发请求数
MAX_CONCUR_REQ = 1 #最大的并发请求数
SERVERS = {
    'REMOTE': 'http://flupy.org/data/flags',
    'LOCAL': 'http://localhost:8001/flags',
    'DELAY': 'http://localhost:8002/flags',
    'ERROR': 'http://localhost:8003/flags',
    }
DEFAULT_SERVER = 'LOCAL'

DEST_DIR = 'downloads\\'
COUNTRY_CODES_FILE = 'country_codes.txt'

def save_flag(img, filename):
    """将requests库抓取到的图片内容保存到磁盘，img参数为resp.content"""
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(img*2000)

def initial_report(cc_list, actual_req, server_label):
    """初始报告，cc_list是国家代码列表，actual_req是实际执行的并发请求数，server_label是SERVERS字典的键"""
    if len(cc_list) <= 10:
        cc_msg = ', '.join(cc_list)
    else:
        cc_msg = 'from {} to {}'.format(cc_list[0], cc_list[-1])
    print('{} site: {}'.format(server_label, SERVERS[server_label]))
    plural = 's' if len(cc_list) != 1 else ''
    print('searching for {} flag{}: {}'.format(len(cc_list), plural, cc_msg))
    plural = 's' if actual_req != 1 else ''
    print('{} concurrent connection{} will be used.'.format(actual_req, plural))

def final_report(cc_list, counter, start_time):
    """最终报告，counter是个计数器，记录了下载成功/失败/not_found各自情况的发生次数"""
    elapsed = time.time() - start_time
    print('-' * 20)
    plural = 's' if counter[HTTPStatus.ok] != 1 else ''
    print('{} flag{} downloaded.'.format(counter[HTTPStatus.ok], plural))
    if counter[HTTPStatus.not_found]:
        print(counter[HTTPStatus.not_found], 'not found')
    if counter[HTTPStatus.error]:
        plural = 's' if counter[HTTPStatus.error] != 1 else ''
        print('{} error{}.'.format(counter[HTTPStatus.error], plural))
    print('elapsed time: {:.2f}s'.format(elapsed)) #整个任务的总耗时

def expand_cc_args(every_cc, all_cc, cc_args, limit):
    """参数类型分别为bool、bool、字符串列表、int"""
    codes = set()
    A_Z = string.ascii_uppercase
    if every_cc:
        codes.update(a + b for a in A_Z for b in A_Z)
    elif all_cc:
        with open(COUNTRY_CODES_FILE, 'rt') as fp:
            text = fp.read()
        codes.update(text.split())
    else:
        for cc in (c.upper() for c in cc_args):
            if len(cc) == 1 and cc in A_Z:
                codes.update(cc + c for c in A_Z)
            elif len(cc) == 2 and all(c in A_Z for c in cc): #如果cc为2个字符，且这2个字符都是大写字母
                codes.add(cc)
            else:
                msg = 'each CC argument must be A to Z or AA to ZZ.'
                raise ValueError('*** Usage error: ' + msg)
    return sorted(codes)[:limit] #排序后的国家代码组成的集合

def process_args(default_concur_req):
    """定义命令行参数"""
    server_options = ', '.join(sorted(SERVERS)) #4个服务器key选项排序后连成一个字符串
    parser = argparse.ArgumentParser(description='download flags for country codes. default: top 20 countries by population.')
    parser.add_argument('cc', metavar='CC', nargs='*', help='country code or 1st letter(eg. B for BA...BZ)')
    #解析出来的cc参数，将是一个包含0-n个国家代码的列表
    parser.add_argument('-a', '--all', action='store_true', help='get all available flags(AD to ZW)')
    parser.add_argument('-e', '--every', action='store_true', help='get flags for every possible code (AA...ZZ)')
    parser.add_argument('-l', '--limit', metavar='N', type=int, help='limit to N first codes', default=sys.maxsize)
    #最多下载多少张图片；64位解释器下，sys.maxsize==2^63，表示这么大的整数正好要占用8个字节
    parser.add_argument('-m', '--max_req', metavar='CONCURRENT', type=int, default=default_concur_req, help='maximum concurrent requests (default={})'.format(default_concur_req))
    parser.add_argument('-s', '--server', metavar='LABEL', default=DEFAULT_SERVER, help='server to hit; one of {} (default={})'.format(server_options, DEFAULT_SERVER))
    parser.add_argument('-v', '--verbose', action='store_true', help='output detailed progress info')
    args = parser.parse_args() #args是个具名元组，该具名元组的字段名就是这里定义的形参，字段值就是在命令行中输入的实参

    if args.max_req < 1:
        print('*** usage error: --max_req CONCURRENT must be >=1')
        parser.print_usage()
        sys.exit(1)
    if args.limit < 1:
        print('*** usage error: --limit N must be >=1')
        parser.print_usage()
        sys.exit(1)
    args.server = args.server.upper()
    if args.server not in SERVERS: #添加命令行参数时，直接加个choices选项更方便？？
        print('*** usage error: --server LABEL must be one of', server_options)
        parser.print_usage()
        sys.exit(1)
    try:
        cc_list = expand_cc_args(args.every, args.all, args.cc, args.limit)
        #根据-a、-e、-l命令行参数，生成待下载国旗的国家代码组成的集合，该集合将直接用于requests爬虫
    except ValueError as exc:
        print(exc.args[0])
        parser.print_usage()
        sys.exit(1)
    if not cc_list:
        cc_list = sorted(POP20_CC)
    return args, cc_list

def main(download_many, default_concur_req, max_concur_req):
    args, cc_list = process_args(default_concur_req)
    actual_req = min(args.max_req, max_concur_req, len(cc_list))
    initial_report(cc_list, actual_req, args.server)
    base_url = SERVERS[args.server]
    t0 = time.time()
    counter = download_many(cc_list, base_url, args.verbose, actual_req) #counter是一个计数器/collections.Counter()
    assert sum(counter.values()) == len(cc_list), 'some downloads are unaccounted for' #断言语句，如果没有下载到全部国旗，就触发异常
    final_report(cc_list, counter, t0)
