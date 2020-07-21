import face_recognition
import os
import datetime
import numpy as np

def absolute_loss(a, b):
	return np.sum(np.absolute(np.array(a) - np.array(b)))

def test_encoding():
	for img in os.listdir(os.path.join('data', 'algorithm_test')):
		image = face_recognition.load_image_file(os.path.join('data', 'algorithm_test', img))
		boxes1 = face_recognition.face_locations(image, model='cnn')
		boxes2 = face_recognition.face_locations(image)
		loss = absolute_loss(boxes1, boxes2)
		print('图片', img, '通过测试', end='  ')
		print('hog定位:', boxes2, ', cnn定位:', boxes1, ', 绝对值误差:', loss)

if __name__ == '__main__':
	begin = datetime.datetime.now()
	test_encoding()
	print('总共用时:', (datetime.datetime.now() - begin), 's')

