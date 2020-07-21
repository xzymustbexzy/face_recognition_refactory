import os

class name_format(object):

    def __init__(self, separator, id_index, name_index):
        self.separator = separator
        self.id_index = id_index
        self.name_index = name_index

    def get_name(self, file_name):
        return file_name.split(self.separator)[self.name_index]

    def get_id(self, file_name):
        return file_name.split('/')[-1].split(self.separator)[self.id_index]

    def get_filename(self, filename):
        return os.path.splitext(filename)[0]

    def get_postfix(self, filename):
        return os.path.splitext(filename)[1]

    def get_full_filename(self, path):
        return os.path.basename(path)


nf = name_format(separator='_', id_index=2, name_index=3)


if __name__ == '__main__':
    full_filename = nf.get_full_filename('data/batch_check_10/000000_备班_117242_张书杰.jpg')
    id = nf.get_id(full_filename)
    print(id)