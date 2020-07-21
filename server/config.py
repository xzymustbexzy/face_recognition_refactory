# !/usr/bin/env python
# coding=utf-8
# @Author: Xiao Ziyang
# @Description: 数据库与系统的配置参数

# # 调试模式是否开启
DEBUG = True
# 数据库立即读写
SQLALCHEMY_TRACK_MODIFICATIONS = False
#session必须要设置key
SECRET_KEY='A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
# 数据库URL
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/faceDB'