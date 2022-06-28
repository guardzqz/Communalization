import re
import subprocess
import tempfile
import time

import uiautomator2 as u2

from Logs.log import Loggings
from lib.getConfig import writeConf, getConfig

LOG = Loggings()


class Phonedriver:
    _instance = None
    _single = False

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            LOG.info('调了一个相机实例')
            cls._instance = object.__new__(cls)
            cls.getDevicesCamera()
        return cls._instance

    def __init__(self):
        if not self._single:
            self._single = True
            self.u = u2.connect(getConfig("camera", "photo"))

    @classmethod
    def startApp(cls):
        LOG.info('启动APP')
        # 启动包名
        cls().u.app_start(getConfig("cameraPack", "photo"))
        return cls().u

    @classmethod
    def getDriver(cls):
        LOG.info('获取设备对象')
        return cls().u

    @classmethod
    def getDevicesCamera(cls):
        LOG.info('选择设备')
        # 获取设备列表
        plat_v=[re.findall("(.*)\t",i)[0] for i in subprocess.Popen("adb devices", stdin=subprocess.DEVNULL,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()[0].
            decode(encoding='utf-8').split("\r\n") if i and "\t" in i]
        if plat_v:
            print('现有手机序列', plat_v)
            ans = input('要选择哪个手机(1,2...):')
            while True:
                try:
                    if int(ans) and int(ans)<=len(plat_v):
                        camera = plat_v[int(ans)-1]
                        writeConf('camera', camera, 'photo')
                        Phonedriver.hasCameraPack()
                        return
                    else:
                        raise
                except Exception as e:
                    LOG.exception(e)
                    ans = input('要选择哪个手机(1,2...):')
        raise Exception('没找到手机')

    @classmethod
    def hasCameraPack(cls):
        LOG.info('判断相机是否在运行')
        cameraPack = None
        while not cameraPack:
            cameraPack = Phonedriver.getCameraPack()
            if not cameraPack:
                LOG.warning('请打开手机相机...')
                time.sleep(1)
            else:
                writeConf('cameraPack', cameraPack, 'photo')
                return True

    @classmethod
    def getCameraPack(cls):
        LOG.info('获取相机包名')
        out_temp = tempfile.TemporaryFile(mode='w+')
        fileno = out_temp.fileno()
        p = subprocess.Popen(f'adb -s {getConfig("camera", "photo")} shell dumpsys window | findstr mCurrentFocus',
                             shell=True,
                             stdout=fileno, stderr=fileno, encoding='utf-8')
        LOG.info(f'adb -s {getConfig("camera", "photo")} shell dumpsys window | findstr mCurrentFocus')
        try:
            p.wait(timeout=1)
        except Exception as e:
            LOG.exception(e)
        finally:
            p.kill()
        out_temp.seek(0)
        if p.poll() == 0 and out_temp:
            output = out_temp.read()
            out_temp.close()
            LOG.info('output', output)
            if re.findall(r".* (.*?)/", output):
                cameraPack = re.findall(r".* (.*?)/", output)[0]
                if 'camera' in cameraPack:
                    return cameraPack

    @classmethod
    def persistApp(cls):
        LOG.info('保证当前APP的相机')
        while not Phonedriver.getCameraPack():
            Phonedriver.startApp()
            time.sleep(1)


if __name__ == '__main__':
    Phonedriver.getDevicesCamera()