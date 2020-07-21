from API import agent
import os
import json
import threading
from name_format import nf
from data_helper import Data_helper
from colorama import Fore, Back, Style
import datetime

class login_agent(threading.Thread):

    def __init__(self, thread_id, images_path):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.images_path = images_path

    def run(self):
        print ("开始线程：线程" + str(self.thread_id))
        count = self.batch_login()
        print ("退出线程：线程" + str(self.thread_id))
        print('总共注册了' + str(count) + '个用户')

    def batch_login(self):
        id_set = set()
        count = 0
        f = open('./log.txt', 'a')
        for path in self.images_path:         

            full_filename = nf.get_full_filename(path)
            # 获取文件名
            filename = nf.get_filename(full_filename)
            # print(filename)
            # 获取后缀
            postfix = nf.get_postfix(full_filename)
            if postfix not in ('.jpg', '.png', '.jpeg'):
                continue
            name = nf.get_name(file_name=filename)
            id = nf.get_id(file_name=filename)
            # print('准备注册，id == ' + str(id) + 'name == ' + name)
            if id in id_set:
                print('id: ', id, ' 重复！！！！！！！！！！！')
                continue
            res_str = agent.add_face(uid=id, name=name, img_path=path)
            response = json.loads(res_str)

            #若注册成功
            if response['code'] == 0:
                id_set.add(id)
                print('注册成功：id为:' + id + ',' + '姓名为:' + name + ',图片存放路径:' + path + 'message:' + response['message'])
                count += 1
            else:
                print(Fore.RED + '注册失败，图片路径为' + path + ',code == ' + str(response['code']) + 'message:' + response['message'] + '\n')
                print(Style.RESET_ALL, end='')
            

        f.close()
        return count



def test_login():
    dh = Data_helper(file_folder='data/batch_login_100/')
    image_files = dh.read_data()

    thread_num = 4
    splited_files = dh.spliter(files=image_files, thread_num=thread_num)
    threads = []
    for i in range(thread_num):
        thread = login_agent(thread_id=i, images_path=splited_files[i])
        threads.append(thread)

    for i in range(thread_num):
        threads[i].start()

    for i in range(thread_num):
        threads[i].join()

    
    # thread0 = login_agent(0, 'data/考勤数据/2018-10-01/')
    # thread1 = login_agent(1, 'data/考勤数据/2018-10-02/')
    # thread2 = login_agent(2, 'data/考勤数据/2018-10-03/')
    # thread0.start()
    # thread1.start()
    # thread2.start()
    # thread0.join()
    # thread1.join()
    # thread2.join()
    # print('批量注册完成！')

if __name__ == '__main__':
    begin = datetime.datetime.now()
    test_login()
    end = datetime.datetime.now()
    print('用时:', (begin - end))

