import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@47.98.48.168/test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ----------EMAIL相关配置------------#
    # 电子邮箱服务器
    MAIL_SERVER = 'smtp.163.com'
    # 电子邮箱端口，标准端口为25
    MAIL_PORT = 465
    # 电子邮件服务器凭证默认不使用
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    # 电子邮箱服务器用户名
    MAIL_USERNAME = 'se_project_test@163.com'
    # 电子邮箱服务器密码
    MAIL_PASSWORD = 'TJVKEZWVDBNJRQOB'
    # 电子邮箱邮件接收地址
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER = ('ZHQ', 'MAIL_USERNAME')