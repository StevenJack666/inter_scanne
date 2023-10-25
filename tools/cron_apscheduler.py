from apscheduler.triggers.cron import CronTrigger

import time
from apscheduler.schedulers.background import BackgroundScheduler

schedule = BackgroundScheduler()


# 重写Cron定时任务，支持年月日 时分秒的cron表达式
class my_CronTrigger(CronTrigger):
    # def __init__(self, year=None, month=None, day=None, week=None, day_of_week=None, hour=None,
    #              minute=None, second=None, start_date=None, end_date=None, timezone=None,
    #              jitter=None):
    #     super().__init__(year=None, month=None, day=None, week=None, day_of_week=None, hour=None,
    #              minute=None, second=None, start_date=None, end_date=None, timezone=None,
    #              jitter=None)
    @classmethod
    def my_from_crontab(cls, expr, timezone=None):
        values = expr.split()
        if len(values) != 6:
            raise ValueError('Wrong number of fields; got {}, expected 7'.format(len(values)))

        return cls(second=values[0], minute=values[1], hour=values[2], day=values[3], month=values[4],
                   year=values[5], timezone=timezone)


def func_job():
    print(f" Hello world")



if __name__ == '__main__':
    cronStart = "0/10 * * * * *"
    schedule.add_job(func_job, my_CronTrigger.my_from_crontab(cronStart))
    schedule.start()
    count = 1
    while True:
        print('main ' + str(count))
        time.sleep(10)
        count = count + 1
