"""zeroMQ消息队列：发布-订阅模式"""
import argparse
import time
import zmq

def server(context):
    """服务器端：发布套接字"""
    zsock = context.socket(zmq.PUB)
    zsock.bind('tcp://127.0.0.1:5555')
    while True:
        print('发送消息')
        zsock.send_string('消息群发')
        time.sleep(1)

def client(context):
    """客户端：订阅套接字"""
    zsock = context.socket(zmq.SUB)
    zsock.connect('tcp://127.0.0.1:5555')
    zsock.setsockopt_string(zmq.SUBSCRIBE, '') #设置【订阅套接字】的过滤器，空字节串/字符串匹配全部消息
    while True:
        resp = zsock.recv_string()
        print('response: {}'.format(resp))

if __name__ == "__main__":
    context = zmq.Context()
    parser = argparse.ArgumentParser(description='zeroMQ practice')
    parser.add_argument('-c', action='store_true', help='run as the client')
    args = parser.parse_args()
    function = client if args.c else server
    function(context)
