import os
import time
from functools import wraps
import re
from operator import methodcaller

from Logs.log import Loggings
from config.filePath import filePath
from lib.OtherMethod import enableCase
from lib.getConfig import getConfig
from lib.yamlMethod import writeYaml, readYaml
from method.OperationDir import aZip
from method.resultH5 import resultH5

LOG = Loggings()
def caseModule(func):
    def outer(*args, **kwargs):
        LOG.info('开始运行模块前')
        count = 0
        try:
            '''运行类'''
            fun = func(*args, **kwargs)
            '''根据配置决定是否运行方法'''
            allcase = (list(filter(lambda m: not m.startswith("__") and not m.endswith("__") and callable(getattr(func, m)), dir(func))))
            allcase = [int(float(re.findall('test_(.*)', i)[0])) for i in allcase]
            enable = enableCase()
            for i in enable:
                if len(allcase) > 0 and i in allcase:
                    LOG.warning('当前运行函数', 'test_'+str(i))
                    caller = methodcaller('test_'+str(i))
                    caller(fun)
                    count+=1
        finally:
            time.sleep(1)
            resultH5.H5(func.__qualname__)
            aZip()
            LOG.warning('一共运行了用例数/写了的/总共要运行的', str(count) +'/' + str(len(allcase)) +'/' + str(len(enable)))
        LOG.info('所有用例执行后')
    return outer

def caseThe(func):
    '''每次新跑一条用例前，根据方法名写用例编号到yaml文件'''
    @wraps(func)
    def inner(*args, **kwargs):
        LOG.info('当前运行用例', func.__qualname__)
        file = re.findall('(.*)\..*_(.*)', func.__qualname__)
        data = readYaml(filePath.CASETEMP_DIR+os.sep+file[0][0]+'.yaml')
        if data is None:
            data = {}
        data[file[0][1]] = []
        writeYaml(filePath.CASETEMP_DIR+os.sep+file[0][0]+'.yaml', data)
        return func(*args, **kwargs)
    return inner


def runOne(func):
    '''限制方法运行一次'''
    num = [0]
    LOG.info('当前函数：', func.__name__, '限制运行一次')
    @wraps(func)
    def inner(*args, **kwargs):
        if num[0]==0:
            num[0]+=1
            return func(*args, **kwargs)
        return None
    return inner
