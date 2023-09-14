#
# from croniter import croniter
# from datetime import datetime
# import time
#
# def cron_task():
#     from croniter import croniter
#     from datetime import datetime
#     print
#     datetime.now()
#
#     cron = croniter('*/1 * * * * *',start_time=datetime.now())
#     for i in  range(5):
#         next_time=cron.get_next()
#         print(next_time)
#
#     print(cron.get_next(datetime))
#
#
#
# if __name__ == '__main__':
#     cron_task()
#     # ap_scheduler_mouth_cron('2022-10-27 21:53:00', '2025-10-27 21:53:30')
#     # aps_scheduler()
#     # ap_scheduler_minute_cron('2022-10-27 21:53:00', '2022-10-27 21:53:30')
#     count = 1
#     while True:
#         print('main '+str(count))
#         time.sleep(60)
#         count=count+1