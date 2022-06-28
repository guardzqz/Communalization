"""
操作日志记录
https://www.cnblogs.com/poloyy/p/12435089.html
"""
import sys
import time
from loguru import logger

from config.filePath import filePath


t = time.strftime("%Y_%m_%d")

class Loggings:
    __instance = None
    # 删去import logger 之后自动产生的handler，不删除的话会出现重复输出的现象
    logger.remove()
    # 控制台输出等级
    logger.add(sys.stderr, level='INFO')
    # 日志等级
    logger.add(f"{filePath.LOG_DIR}/log_{t}.log", rotation="0:00", encoding="utf-8", enqueue=True,
               retention="1 days", level="INFO")

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Loggings, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def info(self, *msg):
        return logger.info(self.flatData(msg))

    def debug(self, *msg):
        return logger.debug(self.flatData(msg))

    def warning(self, *msg):
        return logger.warning(self.flatData(msg))

    def error(self, *msg):
        return logger.error(self.flatData(msg))

    def exception(self, *msg):
        logger.exception(self.flatData(msg))

    def flatData(self, data):
        temp = ''
        for i in data:
            temp += ' '+str(i)
        return temp

if __name__ == '__main__':
    log = Loggings()
    log.info("中文test",'djdj', 1)
    log.debug("中文test", 'hhhd')
    log.warning("中文test")
    log.error("中文test")
    try:
        print(1/0)
    except Exception as e:
        log.exception(e,11)
    log.info('hhh')
