import os
import configparser


class ReadConf:

    # 程序化入口类
    def __init__(self, file_name='system.inf', path='./', encode='utf-8'):
        self.conf = configparser.ConfigParser()
        self.file_path = os.path.join(path, file_name)
        self.conf.read(self.file_path, encoding=encode)


    def get_value(self, section,key,):
        # 获取配置文件的信息
        return self.conf.get(section, key)

    def get_conf(self):
        return self.conf

    def write_or_update_value(self, section, key, value):
        self.conf.set(section, key, value)
        with open(self.file_path, 'w',encoding='utf-8') as fw:  # 循环写入
            self.conf.write(fw)