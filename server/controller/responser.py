# !/usr/bin/env python
# coding=utf-8
# @Author: Xiao Ziyang
# @Description: 中间件，实现Restful接口

import json

'''
返回对象接口
'''
class Responser(object):
		def wrap(self):
				# 这里利用了python反射机制
				# 实现了直接根据变量构造返回体
				return json.dumps(self.__dict__)



'''
公共的返回对象
'''
class CommonResponser(Responser):
		
		def __init__(self, code, message):
				self.code = code
				self.message = message


'''
check face服务的返回对象
'''
class CheckFaceResponser(CommonResponser):
	
	def __init__(self, code, message):
		super().__init__(code, message)
	
	def wrap(self, uid, uid_type, name, sim, simResult, imgFlowNo, mode):
		self.uid = uid
		self.uid_type = uid_type
		self.name = name
		self.sim = sim
		self.simResult = simResult
		self.imgFlowNo = imgFlowNo
		self.mode = mode
		return super().wrap()




InputIntegrityException = CommonResponser(code=1, message='请求输入参数中，有缺失参数')
SystemParametersException = CommonResponser(code=12, message='系统参数读取错误')
AddFaceSuccess = CommonResponser(code=0, message='注册成功')
FaceAlreadyLoginedException = CommonResponser(code=10, message='该人脸已经注册过了')
CannotFoundFaceException = CommonResponser(code=8, message='找不到图片中的人脸')
FaceAbsentException = CommonResponser(code=9, message='人脸未注册')
CheckFaceSuccess = CheckFaceResponser(code=0, message='成功请求人脸识别服务')