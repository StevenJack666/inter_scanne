import sched, time

s = sched.scheduler(time.monotonic, time.sleep)
def print_time(a='default'):
    print("From print_time", time.time(), a)


def changan():
    print('changan')

def breached():
    s.enter(10, 1, print_time)
    print('breached')

def dark_net():
    print('zhangmm_dark_net')
def print_some_times(delay, priority, func, *args):
    print('enter'+str(time.time()))
    s.enter(delay, priority, func, argument=(args))
    s.run()
    print('exit' + str(time.time()))


if __name__ == '__main__':
    test = print_some_times(10, 0, dark_net)
    test1 = print_some_times(20, 0, changan)
    test2= print_some_times(30, 0, breached)
