#coding=utf-8

import configparser

from Logs.log import Loggings
from config.filePath import filePath

LOG = Loggings()
def getConfig(key,group='config'):
    '''读config文件'''
    LOG.info('读取config', key, group)
    config = configparser.ConfigParser()
    # -read读取ini文件
    config.read(filePath.CONFIG_FILE, encoding='utf-8-sig')
    msg=config.get(group, key)
    return msg


def writeConf(name, arg, group='config'):
    '''
    写入配置文件
    '''
    LOG.info('写入config', name, arg, group)
    conf = configparser.ConfigParser()
    root_path = filePath.CONFIG_FILE
    conf.read(root_path, encoding="utf-8-sig") # 文件路径
    conf.set(group, name, arg)  # 修改指定section 的option
    with open(root_path, 'w+', encoding="utf-8-sig") as f:
        conf.write(f)



if __name__ == '__main__':
    pass