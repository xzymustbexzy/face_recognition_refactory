#!/usr/bin/env python
#coding=utf-8
# @Author: Xiao Ziyang
# @Description: 提供人脸识别服务

from server import app, db
from flask import request
from server import parameters_dic
from server.controller.responser import *
from server.model.Face import Face
from server.model.Log import Log
import base64
import datetime
import face_recognition
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
import os


# 人脸注册服务
@app.route('/faceService/addFaces', methods=['POST'])
def add_face():
	'''
	程序流程：
	1、检查请求参数
	2、解码并保存照片
	3、人脸编码
	4、存数据库
	'''

	# 检查请求参数，同时获取这些数据，赋值给对应变量，如果数值不存在，则返回输入字段缺失错误
	try:
		uid, uid_type, name, channel, encoded_img = get_data(['uid', 'uid_type', 'name', 'channel', 'img'])
	except KeyError:
		return InputIntegrityException.wrap()

	# 给该请求标记一个timestamp，后续作为统一的标记
	timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

	# 生成图片路径，将图片解码并保存
	img_name = gen_img_name(uid, timestamp)

	# 生成图片路径，将图片解码并保存
	img_name = gen_img_name(uid, timestamp)
	try:
		img = decode_img(encoded_img)
		img_path = save_img(img, parameters_dic['login_image_root'], img_name)
	# 读取参数时如果没有login_image_root键，就回报错
	except KeyError:
		return SystemParametersException.wrap()

	# 读取文件夹下的图片，进行人脸编码
	encoded_face = face_encoding(img_path)
	# 找不到人脸时，编码为空
	if encoded_face is None:
		return CannotFoundFaceException.wrap()

	# 保存人脸到数据库
	try:
		save_face(
			uid=uid,
			uid_type=uid_type,
			name=name,
			channel=channel,
			timestamp=timestamp,
			encoded_face=encoded_face,
			img_path=img_path
		)
	# 已经注册过了
	except IntegrityError: 
		return FaceAlreadyLoginedException.wrap()


	return AddFaceSuccess.wrap()




# 人脸验证服务
@app.route('/faceService/checkPerson', methods=['POST'])
def check_person():
	'''
	程序流程：
	1、检查请求参数
	2、读取数据库中对应的图片编码
	3、解码并保存图片
	4、人脸编码
	5、两张照片对比
	6、对比记录存数据库
	'''

	# 检查请求参数，同时获取这些数据，赋值给对应变量，如果数值不存在，则返回输入字段缺失错误
	try:
		uid, uid_type, name, channel, encoded_img = get_data(['uid', 'uid_type', 'name', 'channel', 'img'])
	except KeyError:
		return InputIntegrityException.wrap()
	
	# 给该请求标记一个timestamp，后续作为统一的标记
	timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

	# 生成图片路径，将图片解码并保存
	img_name = gen_img_name(uid, timestamp)

	# 生成图片路径，将图片解码并保存
	img_name = gen_img_name(uid, timestamp)
	try:
		img = decode_img(encoded_img)
		img_path = save_img(img, parameters_dic['check_image_root'], img_name)
	# 读取参数时如果没有login_image_root键，就回报错
	except KeyError:
		return SystemParametersException.wrap()

	# 读取文件夹下的图片，进行人脸编码
	encoded_face = face_encoding(img_path)
	# 找不到人脸时，编码为空
	if encoded_face is None:
		return CannotFoundFaceException.wrap()

	# 读取数据库中的注册人脸
	try:
		logined_face = get_login_face(uid)
	except NoResultFound:
		return FaceAbsentException.wrap()
	if not logined_face:
		return FaceAbsentException.wrap()


	# 将encoded_face（上传的人脸）和logined_face（注册时的人脸）进行比较
	# 返回的sim为相似度，sim_result为对比结果
	sim, result = face_compare(logined_face, encoded_face, parameters_dic['tolerance'])

	print(type(result))

	# 将对比记录存放到数据库
	flow_no = log(
		uid=uid, 
		uid_type=uid_type,
		name=name,
		channel=channel,
		check_time=timestamp,
		img_path=img_path,
		sim=sim,
		result=result
	)

	return CheckFaceSuccess.wrap(sim=sim, simResult=result, imgFlowNo=flow_no)



# 从request对象中获取指定的数据
def get_data(fileds):
	'''
		输入为一个数据的键列表
		输出为一个相应值的迭代器
	'''
	for field in fileds:
		yield request.form[field]


# 将Base64编码的图片解码
def decode_img(encoded_img):
	# 解码
	img = base64.b64decode(encoded_img)
	return img

# 保存图片
def save_img(img, file_dir, file_name):
	# 组合文件路径，保存图片
	file_path = os.path.join(file_dir, file_name)
	# 若文件夹不存在，需要先创建文件夹
	if not os.path.exists(file_dir):
		os.mkdir(file_dir)
	with open(file_path, 'wb') as f:
		f.write(img)
	return file_path


# 生成图片名
def gen_img_name(uid, timestamp):
	img_name = uid + '-' + timestamp + '.jpg'
	return img_name

# 对图片进行编码
def face_encoding(img_path):
	# 从文件中加载图片
	img = face_recognition.load_image_file(img_path)
	# 用hog进行人脸定位
	boxes = face_recognition.face_locations(img, model='hog')
	if len(boxes) == 0:
		print('WARNING:using CNN!')
		boxes = face_recognition.face_locations(img, model='cnn')
	# 返回的是一个列表，这里只需要一个
	encoded_faces = face_recognition.face_encodings(img, boxes)
	if len(encoded_faces) > 0:
		return encoded_faces[0]
	return None


# 保存人脸编码与对应的人的信息
def save_face(uid, uid_type, name, channel, timestamp, encoded_face, img_path):
	user = Face(
		uid=uid, 
		uid_type=uid_type, 
		name=name, 
		channel=channel, 
		feature_array=encoded_face,
		login_time=timestamp, 
		img_path=img_path
	)
	db.session.add(user)
	db.session.commit()


# 获取数据库中保存的人脸
def get_login_face(uid):
	face = Face.query.filter_by(uid=uid).first()
	return face


def face_compare(logined_face, encoded_face, tolerance):
	logined_face_encoding = logined_face.feature.split('|')
	logined_face_encoding = list(map(lambda x: float(x), logined_face_encoding))
	face_distance = float(face_recognition.face_distance([logined_face_encoding], encoded_face)[0])
	sim_result = '1' if face_distance < tolerance else '0'
	sim = 1 - face_distance
	return sim, sim_result

def log(uid, uid_type, name, channel, check_time, img_path, sim, result):
	log = Log(
		uid=uid, 
		uid_type=uid_type, 
		name=name, 
		channel=channel, 
		check_time=check_time, 
		img_path=img_path, 
		sim=sim, 
		result=result
	)
	db.session.add(log)
	# 提交之前flush，可以获取自增的流水号
	db.session.flush()
	flow_no = log.num
	db.session.commit()
	return flow_no
	