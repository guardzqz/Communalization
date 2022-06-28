import os
import time

import cv2

from Logs.log import Loggings
from config.filePath import filePath
from photo.phone.photoMethod import photoMethod
from photo.usb.usbServer import usbServer

from photo.usb.usbvideomethod import VideoCamera

LOG = Loggings()
def increase():
    '''
    #定义一个还有自然数算法的生成器,企图使用next来完成不断调用的递增
    :return:
    '''
    while True:
        n = time.strftime("%Y%m%d_%H%M%S", time.localtime(time.time()))
        LOG.info('n', n)
        yield n


class usbDriver:

    def __init__(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 0为本地摄像头，1为外接摄像头
        self.num = increase()
        self.photos_server = usbServer()
        self.CAMERA = VideoCamera(self.cap)

    def __del__(self):
        self.release_cap()

    def takePhoto(self):
        '''
        照相
        :return:
        '''
        while True:
            self.ret, self.frame = self.cap.read()
            cv2.namedWindow('video', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('video', self.frame)
            cv2.waitKey(1)
            #非阻塞式接收客户端消息
            try:
                self.conn, addr = self.photos_server.sk_server.accept()
                print(self.conn, addr)
            except BlockingIOError:
                try:
                    client_data = self.conn.recv(1).decode()  # 接收信息
                    LOG.info('usb接收到消息', client_data)

                    if not client_data:
                        continue
                    if client_data == "q":  # 接收信息 == "exit":  # 判断是否退出连接
                        break
                    elif client_data == "p":
                        num = str(next(self.num))
                        LOG.info('拍照', filePath.OPICTURES_DIR + os.sep + num + ".jpg")
                        cv2.imwrite(filePath.OPICTURES_DIR + os.sep + num + ".jpg", self.frame)
                        photoMethod.ImageRatio(num + ".jpg")
                    elif client_data == "s":
                        num = str(next(self.num))
                        self.CAMERA.startRecord(num)
                    elif client_data == "e":
                        self.CAMERA.stopRecord()
                except:
                    pass


    def release_cap(self):
        self.cap.release()  # 释放摄像头
        cv2.destroyAllWindows()  # 释放并销毁窗口


if __name__ == '__main__':

    x = usbDriver()
    x.takePhoto()
