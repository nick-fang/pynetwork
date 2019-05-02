
#import time
#from clockdeco import clock


#@clock
#def snooze(sec, hour, place, person):
#    """snooze doc"""
#    time.sleep(sec)

#@clock
#def factorial(n):
#    return 1 if n<2 else n*factorial(n-1)

#if __name__=="__main__":
#    print('*'*40, 'calling snooze(0.123)')
#    snooze(0.123, '14:37 am', place='hangzhou', person='nick')
#    print('*'*40, 'calling factorial(6)')
#    print('6!=', factorial(6))



import time
from clockdeco_param import clock

@clock(fmt='{name}: {elapsed}s')
def snooze(sec):
    time.sleep(sec)

@clock(fmt='{name}({args}) dt={elapsed:0.3f}s')
def snooze2(sec):
    time.sleep(sec)

for i in range(3):
    snooze(0.123)

for i in range(3):
    snooze2(0.123)
