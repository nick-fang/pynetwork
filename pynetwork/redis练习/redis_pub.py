"""redis发布-订阅练习：发布端"""
import random
import redis

conn = redis.Redis()
cats = ['siamese', 'persian', 'maine coon', 'norwegian forest']
hats = ['stovepipe', 'bowler', 'tam-o-shanter', 'fedora']
for msg in range(10):
    cat = random.choice(cats)
    hat = random.choice(hats)
    print(f'publish: {cat} wears a {hat}')
    conn.publish(cat, hat)
