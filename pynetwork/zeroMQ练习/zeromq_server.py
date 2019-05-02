import random
import time
import zmq

context=zmq.Context()
zsock=context.socket(zmq.PUB)
zsock.bind('tcp://127.0.0.1:6789')
cats=['siamese', 'persian', 'maine coon', 'norwegian forest']
hats=['stovepipe', 'bowler', 'tam-o-shanter', 'fedora']
time.sleep(1)
for msg in range(10):
    cat=random.choice(cats)
    hat=random.choice(hats)
    print(f'publish: {cat} wears {hat}')
    zsock.send_json([cat, hat])
       