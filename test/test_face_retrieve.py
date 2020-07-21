from API import agent
import os
import argparse
import json
import threading
from name_format import nf
from utils import show
from data_helper import Data_helper

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--method', type=str)

args = parser.parse_args()

class check_agent(threading.Thread):

    def __init__(self, thread_id, images_path):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.images_path = images_path

    def run(self):
        print ("开始线程：线程" + str(self.thread_id))
        count = self.batch_check()
        print ("退出线程：线程" + str(self.thread_id))
        print('总共注册了' + str(count) + '个用户')

    def batch_check(self):
        id_set = set()
        count = 0
        f = open('./log.txt', 'a')
        for path in self.images_path:
            full_filename = nf.get_full_filename(path)
            # 获取文件名
            filename = nf.get_filename(full_filename)
            # 获取后缀
            postfix = nf.get_postfix(full_filename)
            if postfix not in ('.jpg', '.png', '.jpeg'):
                continue
            name = nf.get_name(file_name=filename)
            id = nf.get_id(file_name=filename)
            id_set.add(id)
            for each_id in id_set:
                print('准备验证，id == ' + str(each_id) + 'name == ' + name)
                res_str = agent.check_person(uid=each_id, name=name, img_path=path)
                response = json.loads(res_str)
                print(response)

            #若注册成功
            if response['code'] == 0:
                id_set.add(id)
                count = count + 1
                print('验证成功：id为:' + id + ',' + '姓名为:' + name + ',图片存放路径:' + path + 'message:' + response['message'])
            else:
                print('验证失败，图片路径为' + path + ',code == ' + str(response['code']) + 'message:' + response['message'] + '\n')

        f.close()
        return count


def main():
    dh = Data_helper(file_folder='data/batch_check_10/')
    image_files = dh.read_data()

    thread_num = 1
    splited_files = dh.spliter(files=image_files, thread_num=thread_num)
    threads = []
    for i in range(thread_num):
        thread = check_agent(thread_id=i, images_path=splited_files[i])
        threads.append(thread)

    for i in range(thread_num):
        threads[i].start()

    for i in range(thread_num):
        threads[i].join()

if __name__ == '__main__':
    show(args.method)