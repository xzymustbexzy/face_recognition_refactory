import sys
import face_recognition
import numpy as np

# 生成图片名
def gen_img_name(uid, timestamp):
	img_name = uid + '-' + timestamp + '.jpg'
	return img_name


def test_get_img_name():
	assert(gen_img_name(uid='123', timestamp='2018-10-4 10:20:21') == '123-2018-10-4 10:20:21.jpg')
	assert(gen_img_name(uid='', timestamp='') == '-.jpg')
	assert(gen_img_name(uid='jpg', timestamp='2019.1.2 10:3:1') == 'jpg-2019.1.2 10:3:1.jpg')
	assert(gen_img_name(uid='null', timestamp='2018-10-4') == 'null-2018-10-4.jpg')


# 对图片进行编码
def face_encoding(img_path):
	run_path = []

	# 从文件中加载图片
	img = face_recognition.load_image_file(img_path)
	run_path.append('load_img')

	# 用hog进行人脸定位
	boxes = face_recognition.face_locations(img, model='hog')
	run_path.append('hog_location')

	if len(boxes) == 0:
		# print('WARNING:using CNN!')
		boxes = face_recognition.face_locations(img, model='cnn')
		run_path.append('cnn_location')

	# 返回的是一个列表，这里只需要一个
	encoded_faces = face_recognition.face_encodings(img, boxes)
	run_path.append('encoding')

	if len(encoded_faces) > 0:
		run_path.append('found')
		return encoded_faces[0], run_path

	run_path.append('not_found')
	return None, run_path

def print_path(ret_obj):
	print('-->'.join(ret_obj[-1]))
	return ret_obj[-1]

def test_face_encoding():
	assert(print_path(face_encoding('data/face_encoding_test/ambigous1.png')) == ['load_img', 'hog_location', 'cnn_location', 'encoding', 'found'])
	print('ambigous1.png 测试通过')
	assert(print_path(face_encoding('data/face_encoding_test/ambigous2.png')) == ['load_img', 'hog_location', 'cnn_location', 'encoding', 'found'])
	print('ambigous2.png 测试通过')
	assert(print_path(face_encoding('data/face_encoding_test/clear1.jpeg')) == ['load_img', 'hog_location', 'encoding', 'found'])
	print('clear1.jpeg 测试通过')
	assert(print_path(face_encoding('data/face_encoding_test/clear2.jpeg')) == ['load_img', 'hog_location', 'encoding', 'found'])
	print('clear2.jpeg 测试通过')
	assert(print_path(face_encoding('data/face_encoding_test/no_face.jpg')) == ['load_img', 'hog_location', 'cnn_location', 'encoding', 'not_found'])
	print('no_face.jpg 测试通过')
	assert(print_path(face_encoding('data/face_encoding_test/dog.jpg')) == ['load_img', 'hog_location', 'cnn_location', 'encoding', 'not_found'])
	print('dog.jpg 测试通过')
	assert(print_path(face_encoding('data/face_encoding_test/multi_face.jpeg')) == ['load_img', 'hog_location', 'encoding', 'found'])
	print('multi_face.jpeg 测试通过')


def face_compare(logined_face, encoded_face, tolerance):
	logined_face = np.array(logined_face)
	encoded_face = np.array(encoded_face)
	face_distance = float(face_recognition.face_distance([logined_face], encoded_face)[0])
	sim_result = '1' if face_distance < tolerance else '0'
	sim = 1 - face_distance
	return sim, sim_result


def parse_compare_result(logined_face, encoded_face, tolerance, expect_sim, expect_result):
	sim, sim_result = face_compare(logined_face, encoded_face, tolerance)
	print('sim=', sim, ', sim_result=', sim_result)
	assert(abs(sim - expect_sim) < 0.01)
	assert(expect_result == sim_result)


def test_face_compare():
	parse_compare_result([1] * 128, [1] * 128, .001, expect_sim=1, expect_result='1')
	print('test 1 passed!')
	parse_compare_result([0] * 128, [1] * 128, .999, expect_sim=-10.3137, expect_result='0')
	print('test 2 passed!')
	parse_compare_result([0] * 128, [0] * 128, .001, expect_sim=1, expect_result='1')
	print('test 3 passed!')
	parse_compare_result([0.3] * 128, [0.8] * 128, .5, expect_sim=-4.65, expect_result='0')
	print('test 4 passed!')
	parse_compare_result([0.051] * 128, [0.052] * 128, .5, expect_sim=0.98, expect_result='1')
	print('test 5 passed!')
	sim, sim_result = face_compare(np.random.randn(128), np.random.randn(128), .8)
	assert(sim_result == '0')
	assert(sim < -10)
	print('sim=', sim, ', sim_result=', sim_result, end='')
	print('test 6 passed!')
	


test_face_compare()