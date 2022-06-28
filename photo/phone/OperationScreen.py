import os
import subprocess
import time

from Logs.log import Loggings
from config.filePath import filePath
from lib.OtherMethod import writeType
from lib.getConfig import getConfig
from method.OperationDir import writeText
from photo.phone.Phonedriver import Phonedriver
LOG = Loggings()
class OperationScreen:
    _instance = None
    def __new__(cls, *args, **kw):
        if cls._instance is None:
            LOG.info('调了一个录像实例')
            cls._instance = object.__new__(cls)
        return cls._instance

    def kill_adb(self):
        LOG.info('杀死多余的adb tasklist|findstr adb.exe')
        x = subprocess.Popen(f"tasklist|findstr adb.exe", shell=True, stdout=subprocess.PIPE).communicate()[0].decode(
            "utf-8")
        if x.split():
            os.system('TASKKILL /F /IM adb.exe')

    def recodingScreen(self, times=1):
        LOG.info('开始录屏', times)
        self.kill_adb()
        Phonedriver.persistApp()

        #--size 1920x480 录屏尺寸
        #录屏时间最长3分钟
        time.sleep(float(times))
        self.sn = getConfig("camera", "photo")
        self.filename = time.strftime("%Y%m%d_%H%M%S", time.localtime(time.time()))
        adb_cmd= f"adb -s {self.sn} shell screenrecord --bit-rate 1000000  sdcard/{self.filename}.mp4"
        LOG.info('录屏开始', adb_cmd)
        self.handle=subprocess.Popen(adb_cmd)

    def killScreen(self, path, description=None, times=1):
        '''
        :param sn: 手机sn码
        :param filename: 导出mp4文件名称
        :return:
        '''
        LOG.info('结束录屏')
        time.sleep(float(times))
        os.system("taskkill /F /T /PID " + str(self.handle.pid))
        adb_cmd = f"adb -s {self.sn} pull /sdcard/{self.filename}.mp4 {filePath.FVIDEOS_DIR}/{self.filename}.mp4"
        LOG.info('录屏结束', adb_cmd)
        os.system(adb_cmd)
        writeText(filePath.DESCRIPTION, description)
        writeType(path, 's')
