# 1、解压代码包
```
tar -zxvf vcrawl.tar.gz && cd vcrawl
```
解压后的目录结构如下：
```
.
├── README.md
├── __init__.py
├── __pycache__
├── breached.conf
├── changan.conf
├── darknet.conf
├── data
├── handler
├── logs
├── requirements.txt
├── setting.py
├── tools
├── vcrawl.py
└── vcrawl_task.py
```

# 2、准备环境
## 2.1 数据库环境
安装mysql并根据./data/sql 中的 ddl.sql创建表
## 2.2 python环境
```
使用python3.7+环境执行

控制台下载
pip install -r requirements.txt
后台下载
nohup python3.7 -m pip install -r requirements.txt  >vcrawler.log 2>&1 &

python包镜像：https://mirrors.aliyun.com/pypi/simple/
pip3 install cnocr -i https://mirrors.aliyun.com/pypi/simple/
```

## 2.3 
```
添加新的依赖
pip freeze > requirements.txt
```

# 3、更新配置文件
## 3.1 更新mysql与emal账号密码
```
vi ./tools/config.py

内容如下，按照真实情况修改
# mysql配置
mysql_host = "127.0.0.1"
mysql_port = 3306
mysql_usr = "xxx"
mysql_pass = "xxx"
mysql_db = "vcrawl"

# email配置
mail_user = "superchaosos@163.com"
mail_password = "xxx"
mail_host = "smtp.163.com"
mail_port = 465
```

## 3.2 更新任务配置
参考./darknet.conf 和 ./changan.conf 配置任务相关参数
```
vi ./darknet.conf

配置说明如下：
# 表示作业的基本信息
[base]
# 爬虫类型:[darknet] 二选一
type = darknet
# 自类型: darnet包括[trading_net | changan] 二选一
sub_type = trading_net

# 爬虫目标网址参数
[url]
# 协议 http or https
url.protocol = http
url.domain =xxxxxxxxxs6qbnahsbvxbghsnqh4rj6whbyblqtnmetf7vell2fmxmad.onion
# 爬取的最大页数
url.max.pagenum = 10

# 自动登录参数,需要登录的任务才配置
[login]
login.name = 759847
login.passwd = tianqi6997091
# 以下cookies的格式不需要更改,暗网中文网专用
login.cookies.format = PHPSESSID=%s
query.cookies.format = PHPSESSID=%s; userid=%s

# 输出解析参数
[parse]
# 匹配关键词,多个关键词逗号分割
parse.match.keyword = 银行,中国
parse.max.pagenum = 20

[proxy]
tor.port = 9151
proxies.http = socks5h://localhost:9150
proxies.https = socks5h://localhost:9150

[alter]
alter.type = email
# 匹配出的告警结果收件人
alter.mail.toaddrs = zhangchaoss122@163.com
# 程序出问题收件人,建议加上开发者,用来及时发现问题并调试
alter.mail.error.addrs = zhangchaoss122@163.com

# 其它配置参数
[others]
# 运行模式：once:命令提交后仅执行一次。forever:命令提交后会循环执行(直到出错为止)
run_type = once
# 如果 run_type=forever, 此参数生效，每次循环间隔时间,单位:秒
run_interval = 1800
```

# 4、执行命令
至今使用darnet.conf或者changan.conf或者复制新的配置文件，修改执行命令
```
进入py用户
# 暗网交易市场  trade
sudo  nohup python3.7 /home/py/package/backend/vcrawl/vcrawl.py crawl --task_id={} --conf=darknet.conf > /home/py/logs/py_darknet.log 2>&1 &
# 长安不夜城
sudo  nohup python3.7 /home/py/package/backend/vcrawl/vcrawl.py crawl --task_id={} --conf=changan.conf > /home/py/logs/py_changan.log 2>&1 &
#TG爬虫
sudo nohup python3.7 /home/py/package/backend/vcrawl/vcrawl.py  tg --task_id={} --action=get_message >/home/py/logs/py_tg.log  2>&1 &


# 查看日志
less logs/info.log
```
# 5.事件topic数据结构

``` 
        {
            "message_id":"",
            "type":"1",
            "datetime":"1234567890",
            "data": [
                        {
                            "id":"id",
                            "sample_datas":[{
                                "original_event_id":"123",
                                "tenanted_id":"",
                                "phone_num":"",
                                "bind_id":"",
                                "user_name":"",
                                "user_id":"",
                                "identity_id":"",
                                "home_addr":"",
                                "bin_check":"",
                                "luhn_check":""
                                
                            }]
                        }
            ]
        }
```

# 6、特别说明
1. darnet的交易市场可以完成自动登录，只需更改配置文件中的**login.name**和**login.passwd**即可
2. 长安不夜城登录较为复杂，目前需要人工在本地访问，获取request header内的**Authorization**，更新配置文件中的**url.auth.header**
3. 如果需要配置调度，结合crontab配置，注意需要将**run_type**设置成**once**。
4. 由于长安不夜城不能自动登录，如果调度间隔时间过长Authorization会过期(目前2小时内不会过期)，可以将**run_type**设置成**forever**,长期运行。

# 7.构建docker镜像
1.docker build -f Dockerfile -t myselfsql .
2.启动镜像并通过环境变量传参：docker run -it -d --name myimage -e PARAMS="我是参数" my_image
3.启动镜像并使用命令行传参数：docker run myimage command --option1=value --option2=value
4.docker run -itd -p 13306:13306 --name crawl_mysql \
    -v /data/dockerdata/mysql3306/conf/my.cnf:/etc/my.cnf \
    -v /data/dockerdata/mysql3306/log:/var/log --privileged=true \
    --restart=always -e MYSQL_ROOT_PASSWORD=Qzhang450000 -d myselfsql

5.docker run -itd -p 13306:13306 --name crawl_myselfsql \
    -v /data/dockerdata/mysql13306/conf/my.cnf:/etc/my.cnf \
    -v /data/dockerdata/mysql13306/log:/var/log --privileged=true \
    --restart=always -e MYSQL_ROOT_PASSWORD=Qzhang450000 -d myselfsql


# 8.tg 定时任务关键字sql
INSERT INTO tbl_monitor_task (id, task_name, tenant_id, Mon_Tp_Nm, T_FIELD, Acq_Tsk_StTm, Tsk_EdTm_Pnt, Exec_Frq, CRONTAB_EXP_INF, Upload_File_Rte, fileContent,
                                     Ctg_Rule_DSC, DEL_ST, CREATE_TIME, UPDATE_TIME) VALUES (1, '1', 'zhnormal', '1', '1',
                                                                                             '2023-09-01 09:28:40', '2023-09-20 09:28:45',
                                                                                             1, '1', '1', '建行,建设银行,银行,信用卡,贷款,金融,ccb,股票', '1', '1', '2023-09-01 09:29:15', '2023-09-20 15:48:13');