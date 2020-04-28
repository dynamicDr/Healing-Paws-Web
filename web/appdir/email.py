from flask_mail import Message
from appdir import mail, app
from flask import render_template


def send_email(subject, sender, recipients, text_body, html_body):
    """
    发送电子邮件
    :param subject: 标题
    :param sender: 发送者
    :param recipients: 接收者列表
    :param text_body: 纯文本内容
    :param html_body: HTML格式内容
    :return:
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)
'''
https://blog.csdn.net/sdwang198912/java/article/details/89884414
'''

def send_password_reset_email(user):
    """发送密码重置电子邮件"""
    token = user.get_jwt_token()
    send_email('[博客] 重置您的密码',\
               sender = app.config['MAIL_USERNAME'],\
               recipients=[user.email],\
               text_body=render_template('email/reset_password.txt', user=user, token=token),\
               html_body=render_template('email/reset_password.html', user=user, token=token))
