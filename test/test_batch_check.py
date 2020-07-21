from API import agent
import os
import json
import threading
from name_format import nf
from data_helper import Data_helper
from colorama import Fore, Back, Style


class check_agent(threading.Thread):

    def __init__(self, thread_id, images_path, ids):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.images_path = images_path
        self.ids = ids

    def run(self):
        print ("开始线程：线程" + str(self.thread_id))
        count = self.batch_check()
        print ("退出线程：线程" + str(self.thread_id))
        print('总共注册了' + str(count) + '个用户')

    def batch_check(self):
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
            try:
                for id in self.ids:
                    print('准备验证，id == ' + str(id))
                    print(id, ', ', name, ', ', path)
                    res_str = agent.check_person(uid=id, name=name, img_path=path)
                    response = json.loads(res_str)
                    assert(response['code'] == 0)
                    if id == nf.get_id(file_name=filename):
                        assert(response['simResult'] == '1')
                    else:
                        assert(response['simResult'] == '0')
            except AssertionError:
                print(Fore.RED + '断言失败，上传id = ' + id + ',真实id = ', nf.get_id(file_name=filename), '\n')
                print(Style.RESET_ALL, end='')

        f.close()
        return count



if __name__ == '__main__':
    dh = Data_helper(file_folder='data/batch_check_10/')
    image_files = dh.read_data()

    print(dh.id_set)

    thread_num = 1
    splited_files = dh.spliter(files=image_files, thread_num=thread_num)
    threads = []
    for i in range(thread_num):
        thread = check_agent(thread_id=i, images_path=splited_files[i], ids=dh.id_set)
        threads.append(thread)

    for i in range(thread_num):
        threads[i].start()

    for i in range(thread_num):
        threads[i].join()