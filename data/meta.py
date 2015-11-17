import os


class DataDirControl:
    def __init__(self, dir_name, path="data/"):
        self.path = path + dir_name + "/"
        self.meta_path = self.path + "meta.txt"
        if not os.path.exists(self.path):
            os.mkdir(self.path)
            self.init_meta()

    def create_version(self, version=None):
        if version is None:
            version = self.get_last_i()+1
        ver_path=self.path+str(version)+"/"
        os.mkdir(ver_path)
        self.increment_last()
        return ver_path

    def get_meta_line(self, option):
        with open(self.meta_path, 'rb') as fp:
            for line in fp:
                dig = line.strip().split('-')
                if dig[0] == option.lower():
                    return int(dig[1])

    def get_last_i(self):
        return self.get_meta_line('last')

    def get_best_i(self):
        return self.get_meta_line('best')

    def update(self, update_fun, who=['best', 'last']):
        with open(self.meta_path, 'rb') as fp:
            lines = [line for line in fp]
        newlines = []
        with open(self.meta_path, 'wb') as fp:
            for line in lines:
                dig = line.strip().split('-')
                if dig[0] in who:
                    dig[1] = str(update_fun(int(dig[1])))
                    newline = '-'.join(dig) + '\n'
                else:
                    newline = line
                newlines.append(newline)
            fp.writelines(newlines)

    def increment(self, who=None):
        self.update(lambda x: x + 1, [who])

    def increment_last(self):
        self.increment('last')

    def init_meta(self):
        with open(self.meta_path, 'wb') as fp:
            fp.writelines(['last-0\n', 'best-0\n'])
