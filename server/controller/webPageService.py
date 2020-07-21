# !/usr/bin/env python
# coding=utf-8
# @Author: Xiao Ziyang
# @Description: 前端页面服务

from server import app
from flask import url_for, render_template, redirect, request
from server import parameters_dic
import json


@app.route('/admin/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/admin/login', methods=['POST'])
def login():
    return redirect('admin/parameters')

@app.route('/admin/parameters', methods=['GET'])
def parameters_page():
    return render_template('parameters.html')
    

@app.route('/admin/faces', methods=['GET'])
def faces_page():
    return render_template('faces.html')


@app.route('/admin/checkLogs', methods=['GET'])
def log_page():
    return render_template('checkLogs.html')

@app.route('/client', methods=['GET'])
def client_page():
    return render_template('client.html')