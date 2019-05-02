"""yield from语句由浅入深
参考《流畅的python》16.7节中引用的PEP 380的术语：
委派生成器，即包含【ret = yield from sub_gen】语句的生成器函数
子生成器，即sub_gen，yield from的操作对象，通常只包含yield语句
调用方/客户端，即直接调用委派生成器的代码（创建、预激、send等），通常就是主程序

分清yield和yield from：
A = yield B，不是一个赋值语句，等号右侧也不是一个表达式
A = yield from B，是一个真正的赋值语句，等号右侧是个真正的表达式"""

def coro1():
    """传递子生成器的产出/yield值"""
    yield from 'ab'

foo=coro1() #创建委派生成器
next(foo) #预激委派生成器
next(foo) #'ab'不是生成器，没有send方法，因此foo.send('hello')会报错
#yield from本身也是一种yield语句
next(foo) #无值可产/yield后，coro1函数定义体执行完毕，就会触发【终止迭代】异常


def coro2():
    """传递子生成器的产出/yield值，捕获子生成器的返回/return值"""
    ret = yield from (i for i in 'ab') #生成器推导式返回一个子生成器
    print('ret ==', ret) #该子生成器（函数）中没有return语句，所以其返回值默认为None

foo=coro2() #创建委派生成器
next(foo) #预激委派生成器
#子生成器具有send方法，因此可以使用【子生成器.send('hello')】
foo.send('hello') #但是发送给子生成器的'hello'不会被赋值给任何变量
foo.send('world') #发送给子生成器的'world'也不会被赋值给任何变量


def subcoro():
    """可以接收客户端send值的子生成器"""
    recv1 = yield 'a' #中断第一次
    recv2 = yield 'b' #中断第二次
    result = recv1 + ' ' + recv2
    #包含返回/return值的【迭代终止】异常会传回委派生成器并被yield from捕获，
    #返回值作为【yield from表达式】的值，在这之后，委派生成器才能重新获得代码执行权
    return result

def coro3():
    """转发子生成器的产出/yield值，转发客户端的发送/send值，捕获子生成器的返回/return值"""
    #从yield from开始执行，到子生成器返回/return值的期间，
    #委派生成器只能作为一根“管道”，被动地在两方之间转发/传递数据，完全丧失代码执行权
    subcoro_ret = yield from subcoro()
    print('finally I, coro3 get the execution rights of code!')
    print('subcoro_ret ==', subcoro_ret)

foo = coro3() #创建委派生成器
next(foo) #预激委派生成器
foo.send('hello') #通过委派生成器，向子生成器发送'hello'
foo.send('world') #向子生成器发送'world'；子生成器中再无yield语句，代码执行权返回到委派生成器
