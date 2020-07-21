from urllib import parse, request
import json
import base64
import datetime

'''
Agent是一个代理，相当于一个代替测试程序去完成真正请求工作的类
'''
class Agent(object):
    HOST = 'localhost'
    PORT = '5050'
    ROOT_PATH = '/faceService/'
    URL = 'http://' + HOST + ':' + PORT + ROOT_PATH

    # 向特定url提交一个请求
    def _post(self, url, data):
        req = request.Request(url=url, data=data)
        res = request.urlopen(req)
        res = res.read()
        return res

    # 向特定url获取一个请求
    def _get(self, url):
        req = request.Request(url=url)
        res = request.urlopen(req)
        res = res.read()
        return res

    # 将数据编码
    def _stringnify(self, data):
        data = parse.urlencode(data).encode('utf-8')
        return data

    # 读取图片，并以base64格式编码
    def _read_img(self, img_path):
        img = open(img_path, "rb")
        img_encoding = base64.b64encode(img.read())
        img.close()
        return img_encoding

    def _generate_data(self, uid, name, img_encoding):
        data = {}
        data['uid'] = uid
        data['uid_type'] = '工号'
        data['name'] = name
        data['channel'] = '测试程序'
        data['login_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data['img'] = img_encoding
        return data

    # 模拟注册事件
    def add_face(self, uid, name, img_path):
        img_encoding = self._read_img(img_path)
        url = self.URL + 'addFaces'
        data = self._generate_data(uid, name, img_encoding)
        data = self._stringnify(data)
        res = self._post(url, data)
        return res

    # 模拟验证事件
    def check_person(self, uid, name, img_path, mode='1v1'):
        img_encoding = self._read_img(img_path)
        url = self.URL + 'checkPerson'
        data = self._generate_data(uid, name, img_encoding)
        data['mode'] = mode
        data = self._stringnify(data)
        res = self._post(url, data)
        return res


# 创建agent对象，用于其它模块的导入
agent = Agent()


'''
简单的测试代码
'''
def test_login():
    response = agent.add_face('2016112678', 'xiaoziyang', './data/simple_test/个人照片.jpg')
    response = json.loads(response)
    print(response)

def test_check():
    response = agent.check_person('2016112678', 'xiaoziyang', './data/simple_test/checkin.jpg', mode='1v1')
    response = json.loads(response)
    print(response)


if __name__ == '__main__':
    # test_login()
    test_check()
