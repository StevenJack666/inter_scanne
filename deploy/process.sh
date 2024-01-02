# crontab -e
# crontab -u username -l

# 0 3 * * * /bin/bash /root/crawl_email/vcrawl/cron_dark.sh >> /root/crawl_email/vcrawl/logs/cron.log 2>&1 &
# 0 3 * * * /bin/bash /root/crawl_email/vcrawl/cron_changan.sh >> /root/crawl_email/vcrawl/logs/cron.log 2>&1 &


source ~/.bashrc
conda init bash
source  activate  crawl
cd /home/py/package/vcrawl
nohup python vcrawl.py  tg --task_id=1 --action=get_message > /home/py/package/install/logs/py_tg.log 2>&1 &
pid=`ps ax | grep vcrawl | grep -v grep | awk -e '{print $1}'`
#echo $pid >> /home/py/package/install/logs/process.log
data_time=`date '+%Y-%m-%d %H:%M:%S'`
line='__'
echo ${data_time}${line}${pid}  >> /home/py/package/install/logs/process.log