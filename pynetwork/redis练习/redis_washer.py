"""redis消息队列练习：生产者"""
import redis
conn = redis.Redis()
print('washer is starting')
dishes = ['salad', 'bread', 'entree', 'dessert']
for dish in dishes:
    msg = dish.encode('utf-8')
    conn.rpush(b'dishes', msg) #向名为“dishes”的redis队列的右侧加入一个msg消息
    print('washed', dish)
conn.rpush(b'dishes', b'quit') #前面是添加字节串，为何这里就添加字符串了？？
print('washer is done')
