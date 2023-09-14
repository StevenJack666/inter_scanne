import time
from apscheduler.schedulers.background import BackgroundScheduler

from tools.cron_apscheduler import my_CronTrigger

schedule = BackgroundScheduler()


#  https://blog.csdn.net/weixin_44799217/article/details/127353134
def job(method_name):
    print('zhangmm job 3s/n ' + method_name)


def func_job():
    print(f" Hello world")


def func_job_cron(method_name):
    print(f" Hello world cron")


'''
每个月一号凌晨一点触发
'''


def ap_scheduler_mouth_cron(func, start_time, end_time):
    # 在每年 1-3、7-9 月份中的每个星期一、二中的 00:00, 01:00, 02:00 和 03:00 执行 task 任务
    schedule.add_job(func, 'cron', args={"leo"}, month='1-12', day='1', hour='10', minute='29', id='test_job1',
                     start_date=start_time, end_date=end_time)
    schedule.start()


'''
每天凌晨一点触发
'''


def ap_scheduler_day_cron(func, start_time, end_time):
    # 周一到周日的1.05分执行
    schedule.add_job(func, 'interval', hours=24, start_date=start_time, end_date=end_time)
    schedule.start()


'''
每小时触发一次
'''


def ap_scheduler_hour_cron(func, start_time, end_time):
    # 每小时的第一分钟执行一次
    schedule.add_job(func, 'interval', hours=1, start_date=start_time, end_date=end_time)
    schedule.start()


'''
每分钟触发一次
'''


def ap_scheduler_minute_cron(id, fun, *args, start_time, end_time):
    # 每小时的第分钟执行一次
    # schedule.add_job(job, 'interval', seconds=60)
    schedule.add_job(fun, 'interval', args, seconds=60, start_date=start_time, end_date=end_time, id=id)
    schedule.start()


'''
获取任务列表
'''


def task_list():
    # 自定义获取所有任务的ID和name列表
    if schedule.get_jobs():
        JobIDList = [x.id for x in schedule.get_jobs()]  # 生成当前所有任务的ID列表
        JobNameList = [x.name for x in schedule.get_jobs()]  # 生成当前任务的作业名称列表，即调用的任务函数名称，如myjob
        print(JobIDList)
        print(JobNameList)


'''
校验任务是否存在
'''


def check_task(myjob):
    if not schedule.get_job('my_job_id'):  # my_job_id为作业的ID号
        schedule.add_job(myjob, 'interval', seconds=3, id='my_job_id')  # 第一个参数为任务函数名称


'''
删除任务
'''


def delete_task(job_id):
    schedule.remove_job(job_id)


'''
执行cron表达式
'''


def cron_task(func_job, job_id, cron, *args):
    schedule.add_job(func_job, my_CronTrigger.my_from_crontab(cron), args, id=job_id)
    # schedule.start()


if __name__ == '__main__':
    ap_scheduler_minute_cron('test_job', job, 'test', start_time='2022-10-27 21:53:00', end_time='2025-10-27 21:53:30')
    cronStart = "0/10 * * * * *"
    cron_task(func_job_cron, '张明明', cronStart, 'test')

    task_list()

    # ap_scheduler_mouth_cron('2022-10-27 21:53:00', '2025-10-27 21:53:30')
    # aps_scheduler()
    # ap_scheduler_minute_cron('2022-10-27 21:53:00', '2022-10-27 21:53:30')
    count = 1
    while True:
        print('main ' + str(count))
        time.sleep(60)
        count = count + 1
