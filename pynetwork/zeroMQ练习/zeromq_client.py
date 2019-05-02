import json
import zmq

context=zmq.Context()
zsock=context.socket(zmq.SUB)
zsock.connect('tcp://127.0.0.1:6789')
topics=['maine coon', 'persian']
for topic in topics:
    zsock.setsockopt_string(zmq.SUBSCRIBE, json.dumps([topic])[:5]) #发送过来的json格式本质上也是字符串，因此这里选择自己构造json字符串，并取其前5个字符作为过滤器，比如'["mai'
while True:
    cat, hat=zsock.recv_json()
    print(f'subscribe: {cat} wears {hat}')
