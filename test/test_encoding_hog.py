import face_recognition
import os
import datetime


def test_encoding():
    for img in os.listdir(os.path.join('data', 'algorithm_test')):
        image = face_recognition.load_image_file(os.path.join('data', 'algorithm_test', img))
        encoding = face_recognition.face_encodings(image)
        assert len(encoding) == 1
        assert len(encoding[0]) == 128
        print('编码成功，维度为', len(encoding), '*', len(encoding[0]), end=' ')
        print('图片', img, '通过测试')

if __name__ == '__main__':
    begin = datetime.datetime.now()
    test_encoding()
    print('总共用时:', (datetime.datetime.now() - begin), 's')

