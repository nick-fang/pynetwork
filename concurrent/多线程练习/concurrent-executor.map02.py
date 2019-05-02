from concurrent.futures import ProcessPoolExecutor
import math

PRIMES = [112272535095293,
          112582705942171,
          112272535095293,
          115280095190773,
          115797848077099,
          1099726899285419]

def is_prime(n):
    """判断整数n是否为质数"""
    if n % 2 == 0:
        return False
    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True

if __name__ == "__main__":
    with ProcessPoolExecutor() as executor: #进程池大小默认等于CPU核心数
        for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)): #质数和is_prime函数的返回结果组成的元组
            print(f'{number} is prime: {prime}')
