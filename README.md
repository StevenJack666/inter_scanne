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

pip install -r requirements.txt
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
# 暗网交易市场
nohup python vcrawl.py crawl --conf=darknet.conf 2>&1 &

# 长安不夜城
nohup python vcrawl.py crawl --conf=changan.conf 2>&1 &

# 查看日志
less logs/info.log
```

# 5、特别说明
1. darnet的交易市场可以完成自动登录，只需更改配置文件中的**login.name**和**login.passwd**即可
2. 长安不夜城登录较为复杂，目前需要人工在本地访问，获取request header内的**Authorization**，更新配置文件中的**url.auth.header**
3. 如果需要配置调度，结合crontab配置，注意需要将**run_type**设置成**once**。
4. 由于长安不夜城不能自动登录，如果调度间隔时间过长Authorization会过期(目前2小时内不会过期)，可以将**run_type**设置成**forever**,长期运行。