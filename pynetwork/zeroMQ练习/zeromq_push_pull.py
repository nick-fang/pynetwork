"""zeroMQ消息队列：推送-拉取模式"""
import argparse
import time
import zmq

def producer(context):
    """服务器端：推送套接字"""
    zsock = context.socket(zmq.PUSH)
    zsock.bind('tcp://127.0.0.1:5557')
    time.sleep(2) #分发任务前保持监听状态2秒，保证多个worker进程同时连接上，以均衡负载
    for num in range(10):
        zsock.send_json({'num':num, 'value':num})
        print(f'向workers分发任务：task {num}')

def consumer(context):
    """客户端：先拉取，再处理/运算，后推送；为保证多个workers能够同时并发，该函数应该先于producer启动"""
    receiver = context.socket(zmq.PULL)
    receiver.connect('tcp://127.0.0.1:5557')
    sender = context.socket(zmq.PUSH)
    sender.connect('tcp://127.0.0.1:5558')
    while True:
        data = receiver.recv_json()
        num = data['num']
        result = data['value'] ** 2
        print(f'正在处理task {num}...')
        time.sleep(0.1) #模拟一个耗时的任务处理过程
        sender.send_json({'num':num, 'value':result})

def result_collector(context):
    """服务器端：拉取套接字"""
    zsock = context.socket(zmq.PULL)
    zsock.bind('tcp://127.0.0.1:5558')
    while True:
        data = zsock.recv_json()
        num = data['num']
        result = data['value']
        print(f'task {num}的计算结果是：{result}')

if __name__ == "__main__":
    context = zmq.Context()
    parser = argparse.ArgumentParser(description='zeroMQ practice')
    group = parser.add_mutually_exclusive_group() #创建互斥组，组中的参数无法共存
    group.add_argument('-c', action='store_true', help='run as a consumer')
    group.add_argument('-r', action='store_true', help='run as a result_collector')
    args = parser.parse_args()
    if args.c:
        function = consumer
    elif args.r:
        function = result_collector
    else:
        function = producer #如果命令行中不带参数，就默认运行producer
    function(context)
