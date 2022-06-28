import os
import time

import uiautomator2 as u2

from config.filePath import filePath
from lib.OtherMethod import writeType
from lib.getConfig import getConfig
from method.OperationDir import writeText


class App:
    def __init__(self, path):
        pass
        self.a2 = u2.connect(getConfig('deviceid', 'app'))
        self.a2.app_start(getConfig('packname', 'app'))
        self.path = path

    def realmesyncapp(self):
        while not self.a2(text='首页').exists():
            self.a2.press('back')
        self.a2(text='首页').click()
        while not self.a2(resourceId='com.techlife.wear.R100:id/sync_progress_bar').exists():
            print('开始同步')
            self.a2.swipe_ext("down", 0.7)
            if self.a2(resourceId='com.techlife.wear.R100:id/sync_progress_bar').exists():
                while not self.a2(resourceId="com.techlife.wear.R100:id/img_left").exists():
                    time.sleep(1)
                    print('同步中')
                print('同步成功')
                return

    def sportdata(self, text=None):
        pass
        self.realmesyncapp()
        print(self.a2(resourceId='com.techlife.wear.R100:id/card_out', text='运动记录').exists())
        while not self.a2(text='运动记录').exists():
            self.a2.press('back')
        self.a2(text='运动记录').click()
        time.sleep(1)
        self.appScreen(text)
        recordlist = self.a2(resourceId='com.techlife.wear.R100:id/rv_item')
        print(len(recordlist), recordlist)
        recordlist[0].click()
        for _ in range(2):
            time.sleep(1)
            self.appScreen(text)
            self.a2.swipe(0.8, 0.8, 0.8, 0.1)

    def appScreen(self, text=None):
        print('屏幕截图', text)
        self.a2.screenshot(
            filePath.FPICTURES_DIR + os.sep + time.strftime("%Y%m%d_%H%M%S", time.localtime(time.time())) + ".jpg")
        writeText(filePath.DESCRIPTION, text)
        writeType(self.path, 'p')

    def veryfitsyncapp(self):
        pass
        while not self.a2(text='健康数据').exists():
            self.a2.press('back')
        self.a2(resourceId='com.watch.life:id/img_home_device').click()
        time.sleep(10)

    def verysport(self, text=None):
        self.veryfitsyncapp()
        self.a2(resourceId='com.watch.life:id/img_sport_record').click()
        time.sleep(1)
        self.appScreen(text)
        recordlist = self.a2(resourceId='com.watch.life:id/iv_sport')
        if len(recordlist):
            recordlist[0].click()
        for _ in range(2):
            time.sleep(1)
            self.appScreen(text)
            self.a2.swipe(0.8, 0.8, 0.8, 0.1)


if __name__ == '__main__':
    a = App(r'D:\zqz\project\dec\config\caseTemp\sport.yaml')
    # a.syncapp()
    # a.sportdata()
    a.verysport()