"""
This is the "example" module.
The example module supplies one function, factorial().  For example,
>>> factorial(5)
120
"""
import math
import doctest

def factorial(n):
    """return the factorial of n, an exact integer >=0
    >>> [factorial(n) for n in range(6)]
    [1, 1, 2, 6, 24, 120]
    >>> factorial(30)
    265252859812191058636308480000000
    >>> factorial(-1)
    Traceback (most recent call last):
        ...
    ValueError: n must be >= 0

    factorials of floats are OK, but the float must be an exact integer:
    >>> factorial(30.1)
    Traceback (most recent call last):
        ...
    ValueError: n must be exact integer
    >>> factorial(30.0)
    265252859812191058636308480000000

    it must also not be ridiculously large:
    >>> factorial(1e100)
    Traceback (most recent call last):
        ...
    OverflowError: n is too large
    """
    if not n >= 0:
        raise ValueError('n must be >= 0')
    if math.floor(n) != n:
        raise ValueError('n must be exact integer')
    if n+1 == n: #捕获过大的n
        raise OverflowError('n is too large')
    result=1
    factor=2
    while factor <= n:
        result *= factor
        factor += 1
    return result

if __name__ == "__main__":
#    doctest.testmod() #使用本模块中的文档字符串作为测试用例
    doctest.testfile('example.txt') #使用参数指定的文本文件中的字符串内容，作为本模块函数和类的测试用例
