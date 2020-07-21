# !/usr/bin/env python
# coding=utf-8
# @Author: Xiao Ziyang
# @Description: 服务器ajax数据服务

from server import app, db
from server.model.Face import Face
from server.model.Log import Log
from server import parameters_dic
from flask import request
import datetime
import json
import base64


@app.route('/admin/restart', methods=['GET'])
def restart():
	current_file = 'server/controller/remoteRestartLog.py'
	with open(current_file, 'a', encoding='utf-8') as f:
		f.write("'Restart program at time " + str(datetime.datetime.now()) + "'\n")
	return '''success'''


@app.route('/admin/parameters/data', methods=['GET'])
def get_parameters():
	return json.dumps(parameters_dic)


@app.route('/admin/parameters', methods=['POST'])
def set_parameters():
	new_param = request.form.get('data')
	new_param = json.loads(new_param)
	new_param['sim_threshold'] = float(new_param['sim_threshold'])
	with open('server/parameters.json', 'w') as f:
		json.dump(new_param, f, indent=4)
	return '''success'''


@app.route('/admin/faces/data', methods=['GET'])
def get_face():
	return query_all('Face')


@app.route('/admin/log/data', methods=['GET'])
def get_log():
	return query_all('Log')


def query_all(class_name):
	ins_list = eval(class_name).query.all()
	for i in range(len(ins_list)):
		ins_list[i] = ins_list[i].serialize()
	data = {'data': ins_list}
	return json.dumps(data)


@app.route('/admin/image', methods=['POST'])
def get_image():
	path = json.loads(request.form.get('data'))['path']
	print(path)
	try:
		with open(path, "rb") as image_file:
			encoded_string = base64.b64encode(image_file.read())
	except IOError:
		print('WARNING:file open error!')
		return '''failed'''

	return encoded_string
	

# 给出id，查出注册照片路径
@app.route('/admin/image/path/<uid>', methods=['GET'])
def get_image_path(uid):
    path = ''
    try:
        face = Face.query.filter_by(uid=uid).all()
    except BaseException as e:
        # print(e)
        print('WARNING:图片路径查询失败，该id可能尚未注册')
        return path
    
    if (len(face) != 1):
        print('WARNING:图片路径查询失败，出现多个结果')
        return path

    path = face[0].img_path
    return path

