
import time

DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'

def clock(fmt=DEFAULT_FMT):
    def decorate(func):
        def clocked(*_args):
            t0 = time.time()
            _result = func(*_args)
            elapsed = time.time() - t0
            name = func.__name__
            args = ', '.join(repr(i) for i in _args)
            result = repr(_result)
            print(fmt.format(elapsed=elapsed, name=name, args=args, result=result))
            return _result
        return clocked
    return decorate

if __name__ == "__main__":
    @clock()
    def snooze(sec):
        time.sleep(sec)

    for i in range(3):
        snooze(0.123)
