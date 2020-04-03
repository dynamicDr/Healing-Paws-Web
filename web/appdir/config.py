import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@47.98.48.168/test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

