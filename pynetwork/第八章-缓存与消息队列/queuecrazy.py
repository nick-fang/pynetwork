"""代码清单8-3 连接5个不同模块的ZeroMQ消息机制；消息队列技术是用于分布式计算和进程间通信的，但是这里使用5条子线程模拟了5个独立的进程，仅具教学意义"""
import random
import threading
import time
import zmq

B = 32 #random模块产生的随机数的精度

def ones_and_zeros(digits):
    """digits是B*2，即64"""
    binary_digit = bin(random.getrandbits(digits)) #生成一个【能够用64bit表示】的随机整数，并转换成二进制字符串
    return binary_digit.lstrip('0b').zfill(digits) #去掉前缀的【0b】，并用前导0填充成64个字符

def bitsource(zcontext, url):
    """生产随机数，是个服务器端"""
    zsock = zcontext.socket(zmq.PUB) #publish分发
    zsock.bind(url) #绑定pubsub端口
    while True:
        zsock.send_string(ones_and_zeros(B * 2))
        time.sleep(0.01)

def always_yes(zcontext, in_url, out_url):
    """是个客户端？？"""
    isock = zcontext.socket(zmq.SUB) #subscribe订阅消息
    isock.connect(in_url) #连接到pubsub端口
    isock.setsockopt(zmq.SUBSCRIBE, b'00') #设置订阅套接字的【过滤器】
    osock = zcontext.socket(zmq.PUSH) #push推送
    osock.connect(out_url) #连接到pushpull端口
    while True:
        isock.recv_string()
        osock.send_string('Y')

def judge(zcontext, in_url, pythagoras_url, out_url):
    """是个客户端？？"""
    isock = zcontext.socket(zmq.SUB) #subscribe订阅
    isock.connect(in_url) #连接到pubsub端口
    for prefix in (b'01', b'10', b'11'):
        isock.setsockopt(zmq.SUBSCRIBE, prefix) #设置订阅套接字的【过滤器】
    psock = zcontext.socket(zmq.REQ) #request请求
    psock.connect(pythagoras_url) #连接到reqrep端口
    osock = zcontext.socket(zmq.PUSH) #push推送
    osock.connect(out_url) #连接到pushpull端口
    unit = 2 ** (B * 2) #2**64==(2**32)**2，即x或y能够达到的最大值的平方，也是待测扇形的半径
    while True: #isock -> psock -> pythagoras()计算 -> psock -> osock
        bits = isock.recv_string()
        n, m = int(bits[::2], 2), int(bits[1::2], 2) #获取64位的bits字符串的偶数位和奇数位
        psock.send_json((n, m)) #将x和y坐标发送给pythagoras()函数
        sumsquares = psock.recv_json() #从pythagoras()函数处接收计算结果
        osock.send_string('Y' if sumsquares < unit else 'N') #如果位点的x坐标和y坐标的平方和，小于扇形半径的平方，则该位点在扇形内；否则该位点在扇形外

def pythagoras(zcontext, url):
    """根据x和y的坐标值，计算x和y的平方和，即该位点到原点的距离的平方；是个服务器端"""
    zsock = zcontext.socket(zmq.REP) #response响应
    zsock.bind(url) #绑定reqrep端口
    while True:
        numbers = zsock.recv_json()
        zsock.send_json(sum(n * n for n in numbers))

def tally(zcontext, url):
    """统计落在扇形内/外的位点数目；是个服务器端"""
    zsock = zcontext.socket(zmq.PULL) #pull拉取
    zsock.bind(url) #绑定pushpull端口
    p, q = 0, 0
    while True:
        decision = zsock.recv_string()
        q += 1
        if decision == 'Y':
            p += 4
        print(decision, p / q)

def start_thread(function, *args):
    thread = threading.Thread(target=function, args=args)
    thread.daemon = True #创建的5条子线程全部都是死循环，所以没有必要使用join()，而是设置为守护线程，最终随着主线程的结束而被强行终止
    thread.start()

def main(zcontext):
    pubsub = 'tcp://127.0.0.1:6700'
    reqrep = 'tcp://127.0.0.1:6701'
    pushpull = 'tcp://127.0.0.1:6702'
    start_thread(bitsource, zcontext, pubsub)
    start_thread(always_yes, zcontext, pubsub, pushpull)
    start_thread(judge, zcontext, pubsub, reqrep, pushpull)
    start_thread(pythagoras, zcontext, reqrep)
    start_thread(tally, zcontext, pushpull)
    time.sleep(30) #5条子线程都被设置为了【守护线程】，会随着主线程的结束而结束，即主线程休眠30秒后，5+1条线程会一起结束运行

if __name__ == "__main__":
    main(zmq.Context())
