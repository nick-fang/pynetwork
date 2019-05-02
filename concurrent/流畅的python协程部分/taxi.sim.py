"""出租车仿真程序"""
import random
from collections import namedtuple
import queue
import argparse
import time

DEFAULT_NUMBER_OF_TAXIS = 3
DEFAULT_END_TIME = 180
SEARCH_DURATION = 5
TRIP_DURATION = 20
DEPARTURE_INTERVAL = 5
Event = namedtuple('Event', 'time proc action') #time代表事件时刻，proc代表进程实体/出租车编号，action代表事件名

def taxi_process(ident, trips, start_time=0):
    """每次状态变化时，向仿真程序产出一个事件，ident为出租车编号，trips为出租车载客的趟数，start_time为出租车从仓库出发的时刻"""
    e_time = yield Event(start_time, ident, 'leave garage') #每次从主程序.send()过来的e_time，会被用于下一个yield语句产出的event对象中
    for i in range(trips):
        e_time = yield Event(e_time, ident, 'pick up passenger')
        e_time = yield Event(e_time, ident, 'drop off passenger')
    yield Event(e_time, ident, 'going home') #这里的e_time来自于上一条yield语句的左值，该左值由主程序.send()赋值

class Simulator:
    """出租车模拟器，以模拟3辆出租车为例"""
    def __init__(self, procs_map):
        self.events = queue.PriorityQueue() #创建优先队列，用于3个出租车协程产出的各种事件，并且按时间顺序（event_obj[0]）正向排序
        self.procs = dict(procs_map) #创建字典副本，这样不会修改源字典

    def run(self, end_time):
        """调度并显示事件，直到时间结束"""
        #调度各辆出租车的第一个事件
        for _, proc in sorted(self.procs.items()): #self.procs字典的值是出租车的活动进程，即出租车协程
            first_event = next(proc) #预激3个出租车协程
            self.events.put(first_event) #把3个出租车协程产出的“离开车库”事件放进优先队列

        #此次仿真的主循环
        sim_time = 0 #仿真“钟”
        while sim_time < end_time:
            if self.events.empty(): #如果优先队列为空
                print('*** end of events ***')
                break
            current_event = self.events.get() #从优先队列中弹出3个event对象中，时刻最早那一个
            sim_time, proc_id, previous_action = current_event #根据事件获取出租车编号
            print('taxi:', proc_id, proc_id * '  ', current_event)
            active_proc = self.procs[proc_id] #根据出租车编号找到它所属的协程
            next_time = sim_time + compute_duration(previous_action) #该出租车下次事件的时刻=当前时刻+间隔时间
            try:
                next_event = active_proc.send(next_time) #根据下次事件的时刻，获取该出租车协程产出的下次事件的event对象
            except StopIteration:
                del self.procs[proc_id]
            else:
                self.events.put(next_event) #把该出租车下次事件的event对象放进优先队列
        else: #如果没有触发过while循环中的break，即时限内所有出租车都完成了规定的趟数，则打印下面的消息
            msg = '*** end of simulation time: {} events pending ***'
            print(msg.format(self.events.qsize()))

def compute_duration(previous_action):
    """使用指数分布计算活动（当前事件与下次事件之间的过程）耗时"""
    if previous_action in ['leave garage', 'drop off passenger']:
        #活动：四处徘徊，寻找乘客
        interval = SEARCH_DURATION
    elif previous_action == 'pick up passenger':
        #活动：搭载乘客中……
        interval = TRIP_DURATION
    elif previous_action == 'going home':
        interval = 1
    else:
        raise ValueError('Unknown previous_action: {}'.format(previous_action))
    return int(random.expovariate(1 / interval)) + 1 #random.expovariate函数用于生成指数分布的随机数

def main(end_time=DEFAULT_END_TIME, num_taxis=DEFAULT_NUMBER_OF_TAXIS, seed=None):
    """初始化随机生成器，构建过程，运行仿真程序"""
    if seed is not None:
        random.seed(seed) #获得可复现的结果
    #构建一个字典，字典的每个元素的值是一个协程对象，代表1辆出租车的活动进程
    procs_map = {i: taxi_process(i, (i + 1) * 2, i * DEPARTURE_INTERVAL) for i in range(num_taxis)}
    sim = Simulator(procs_map)
    sim.run(end_time)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='taxi fleet simulator.')
    parser.add_argument('-e', '--end_time', type=int, default=DEFAULT_END_TIME, help='simulation end time; default={}'.format(DEFAULT_END_TIME))
    parser.add_argument('-t', '--taxis', type=int, default=DEFAULT_NUMBER_OF_TAXIS, help='number of taxis running; default={}'.format(DEFAULT_NUMBER_OF_TAXIS))
    parser.add_argument('-s', '--seed', type=int, default=None, help='random generator seed (for testing)')
    args = parser.parse_args()
    main(args.end_time, args.taxis, args.seed)
    