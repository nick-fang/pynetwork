"""代码清单8-2 向服务器分配数据的两种模式——数据中的模式与散列值中的位"""
import hashlib

def alpha_shard(word):
    """直接将键的首字母作为缓存分区的依据"""
    if word[0] < 'g': #abcdef
        return 'server0'
    elif word[0] < 'n': #ghijklm
        return 'server1'
    elif word[0] < 't': #nopqrs
        return 'server2'
    else: #tuvwxyz
        return 'server3'

def hash_shard(word):
    """将hash()函数的计算结果作为缓存分区的依据"""
    return 'server{}'.format(hash(word) % 4)

def md5_shard(word):
    """将hashlib.md5()函数的计算结果作为缓存分区的依据"""
    data = word.encode('utf-8')
    return 'server{}'.format(hashlib.md5(data).digest()[-1] % 4)

if __name__ == "__main__":
    source = """
    When storing data into memcached, you can set an expiration time—a maximum number of seconds for memcached to keep the key and value around. After that delay, memcached automatically removes the key from its cache. 
    What should you set this cache time to? There is no magic number for this delay, and it will entirely depend on the type of data and application that you are working with. It could be a few seconds, or it might be a few hours.
    Cache invalidation, which defines when to remove the cache because it is out of sync with the current data, is also something that your application will have to handle. Especially if presenting data that is too old or or stale is to be avoided. 
    Here again, there is no magical recipe; it depends on the type of application you are building. However, there are several outlying cases that should be handled—which we haven’t yet covered in the above example.
    A caching server cannot grow infinitely—memory is a finite resource. Therefore, keys will be flushed out by the caching server as soon as it needs more space to store other things. 
    Some keys might also be expired because they reached their expiration time (also sometimes called the “time-to-live” or TTL.) In those cases the data is lost, and the canonical data source must be queried again. """
    import string
    table = str.maketrans('', '', string.punctuation) #构建去除标点的映射表
    words = set(source.translate(table).split()) #转换成单词集合

    for func in (alpha_shard, hash_shard, md5_shard): #分别使用3种算法决定缓存单词的分区号
        partitions = {'server0':0, 'server1':0, 'server2':0, 'server3':0}
        for word in words:
            partitions[func(word)] += 1 #通过散列算法，将单词（模拟memcached缓存系统的键）换算成分区号，并记录每个分区缓存的单词数
        print(func.__name__, ':')
        for key, value in sorted(partitions.items()):
            print(' {} {} {:.2f}'.format(key, value, value / len(words))) #统计4个分区分别缓存了多少个单词；key是分区号，value是该分区下的单词数
        print()
