"""redis发布-订阅练习：订阅端"""
import redis

conn = redis.Redis()
interested_topics = ['maine coon', 'persian']
sub = conn.pubsub()
sub.subscribe(interested_topics) #订阅感兴趣的主题
for msg in sub.listen():
    #print(repr(msg))
    if msg['type'] == 'message':
        cat = msg['channel']
        hat = msg['data']
        print(f'subscribe: {cat} wears a {hat}')
