# coding=utf-8
import os
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql://{user}:{passwd}@{host}:{port}/{database}'.format(
    user=os.environ['USER'],
    passwd=os.environ['PASSWD'],
    host='localhost',
    port=3306,
    database='haha'
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'dhaidhiahfoeawjfoeafhjoafjoeafhjeofeifieafeow'
