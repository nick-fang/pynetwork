"""zeroMQ消息队列：请求-响应模式"""
import argparse
import zmq

def server(context):
    """服务器端：响应套接字"""
    zsock = context.socket(zmq.REP)
    zsock.bind('tcp://127.0.0.1:5555')
    while True:
        message = zsock.recv_string()
        print('received: {!r}'.format(message))
        zsock.send_string('I am OK!')

def client(context):
    """客户端：请求套接字"""
    zsock = context.socket(zmq.REQ)
    zsock.connect('tcp://127.0.0.1:5555')
    zsock.send_string('are you OK?')
    resp = zsock.recv_string()
    print('response: {!r}'.format(resp))

if __name__=="__main__":
    context = zmq.Context()
    parser=argparse.ArgumentParser(description='zeroMQ practice')
    parser.add_argument('-c', action='store_true', help='run as the client')
    args = parser.parse_args()
    function = client if args.c else server
    function(context)
