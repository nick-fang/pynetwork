
registry=[] #保存注册记录的列表

def register(func):
    registry.append(func) #将函数名添加到记录列表中
    return func #将被包装的函数原样返回

@register
def f1():
    pass
def f2():
    pass

registry





registry=set()
def register(active=True):
    """装饰器的工厂函数"""
    def decorate(func):
        """装饰器"""
        print('running register(active={}) -> decorate({})'.format(active, func))
        if active:
            registry.add(func)
        else:
            registry.discard(func)
        return func
    return decorate

@register(active=False)
def f1(): #相当于【f1=register(active=False)(f1)】
    print('running f1()')

@register()
def f2():
    print('running f2()')

def f3():
    print('running f3()')

registry
