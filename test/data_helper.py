from name_format import nf
import os

class Data_helper(object):
    def __init__(self, file_folder):
        self.file_folder = file_folder
        self.id_set = set()

    def read_data(self):
        image_files = []
        for dirpath, dirnames, filenames in os.walk(self.file_folder):
            for fielname in filenames:
                full_filename = os.path.join(dirpath, fielname)
                postfix = nf.get_postfix(full_filename)
                if postfix not in ('.jpg', '.png', '.jpeg'):
                    continue
                id = nf.get_id(full_filename)
                # 剔除重复id
                if id in self.id_set:
                    print(fielname, '  !!!!!!!!!!')
                    continue
                self.id_set.add(id)
                # print(full_filename)
                image_files.append(full_filename)
                
        return image_files

    def spliter(self, files, thread_num):
        splited_files = []
        for i in range(thread_num):
            splited_files.append(list())

        for i in range(len(files)):
            splited_files[i % thread_num].append(files[i])

        return splited_files

