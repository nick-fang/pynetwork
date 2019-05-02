"""《流畅的python》中的示例：线程版"""
import threading
import itertools
import time
import sys

class Signal:
    go = True

def spin(msg, signal):
    """子线程要执行的函数"""
    write, flush = sys.stdout.write, sys.stdout.flush #write和flush是两个函数名
    for char in itertools.cycle('|/-\\'): #cycle函数返回一个无限迭代器
        status = char + ' ' + msg
        write(status) #向标准输出写入一行消息（无\n换行符）
        flush() #强制刷新标准输出
        write('\x08' * len(status)) #向标准输出写入跟消息长度相等的\b退格符
        time.sleep(0.1) #每次刷新间隔0.1秒
        if not signal.go:
            break
    write(' ' * len(status) + '\x08' * len(status))

def slow_function():
    """假装answer需要耗费一段时间"""
    time.sleep(3)
    return 42

def supervisor():
    """设置子线程，显示线程对象，运行耗时的计算，最后终结子线程"""
    signal = Signal()
    spinner = threading.Thread(target=spin, args=('thinking!', signal))
    print('spinner object:', spinner)
    spinner.start()
    result = slow_function()
    signal.go = False #通过一个全局变量，在主线程中控制子线程中的循环break
    spinner.join()
    return result

def main():
    result = supervisor()
    print('answer:', result) #answer前，已经在前面的supervisor()中终结了thinking子线程
if __name__ == "__main__":
    main()
