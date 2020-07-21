# !/usr/bin/env python
# coding=utf-8
# @Author: Xiao Ziyang
# @Description: 系统初始化程序

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import server.config
import json

app = Flask(__name__, static_folder='../', static_url_path='')
app.config.from_object(server.config)
db = SQLAlchemy(app)

# 读取参数列表
with open('server/parameters.json', 'r') as parameters:
    parameters_dic = json.load(parameters)
# tolerance等于：1-相似度阈值
parameters_dic['tolerance'] = 1 - float(parameters_dic['sim_threshold'])


from server.model import Face, Log
from server.controller import faceService, dataService, webPageService, remoteRestartLog