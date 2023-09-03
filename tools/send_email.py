#!/usr/bin/env python
# coding=utf-8
import os
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from tools.config import Config

def send_mail(message,Subject,sender_show,recipient_show,to_addrs,cc_show='', attack_file = ''):
    '''
    :param message: str 邮件内容
    :param Subject: str 邮件主题描述
    :param sender_show: str 发件人显示，不起实际作用如："xxx"
    :param recipient_show: str 收件人显示，不起实际作用 多个收件人用','隔开如："xxx,xxxx"
    :param to_addrs: str 实际收件人
    :param cc_show: str 抄送人显示，不起实际作用，多个抄送人用','隔开如："xxx,xxxx"
    '''
    # 填写真实的发邮件服务器用户名、密码
    user = Config.mail_user
    password = Config.mail_password
    # 邮件内容
    msg = MIMEMultipart()
    msg.attach(MIMEText(message, 'html', _charset="utf-8"))
    # 构造附件1，传送当前目录下的 test.txt 文件
    if attack_file:
        att = MIMEApplication(open(attack_file, 'rb').read())
        att["Content-Type"] = 'application/octet-stream'
        # # 附件名称为中文时的写法
        # att.add_header("Content-Disposition", "attachment", filename=("gbk", "", filename))
        # 附件名称非中文时的写法,这里的filename可以任意写，写什么名字，邮件中显示什么名字
        att["Content-Disposition"] = 'attachment; filename="{}"'.format(os.path.basename(attack_file))
        msg.attach(att)
    # 邮件主题描述
    msg["Subject"] = Subject
    # 发件人显示，不起实际作用
    msg["from"] = user
    # 收件人显示，不起实际作用
    msg["to"] = recipient_show
    # 抄送人显示，不起实际作用
    msg["Cc"] = cc_show
    with SMTP_SSL(host=Config.mail_host,port=Config.mail_port) as smtp:
        # 登录发送邮件服务器
        smtp.login(user = user, password = password)
        # 实际发送、接收邮件配置
        smtp.sendmail(from_addr = user, to_addrs=to_addrs.split(','), msg=msg.as_string())

if __name__ == "__main__":
    message = '''
    <p>Python 邮件发送测试...</p>
    <p><a href="https://www.baidu.com">纵里寻她千百度</a></p>
    '''
    subject = '主题测试'
    # 显示发送人
    sender_show = 'zc'
    # 显示收件人
    recipient_show = 'zc'
    # 实际发给的收件人
    to_addrs = 'superchaosos@163.com'
    send_mail(message,subject,sender_show,recipient_show,to_addrs)