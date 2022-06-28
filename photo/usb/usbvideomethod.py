import os

import threading
import time

import cv2

from Logs.log import Loggings
from config.filePath import filePath

threadLock = threading.Lock()
LOG = Loggings()
class RecordingThread(threading.Thread):
    def __init__(self, name, camera):
        super(RecordingThread, self).__init__()
        self.name = name
        self.cap = camera
        self.isRunning = True
        w = int(self.cap.get(3))  # 获取视频的width
        h = int(self.cap.get(4))

        fourcc = cv2.VideoWriter_fourcc(*'H264') #设置视频编码方式
        self.out = cv2.VideoWriter(filePath.FVIDEOS_DIR + os.sep + f'{name}.mp4', fourcc, 9.5, (w, h))
        # out 是VideoWriter的实列对象，就是写入视频的方式，第一个参数是存放写入视频的位置，
        # 第二个是编码方式，20是帧率，最后是视频的高宽，如果录入视频为灰度，则还需加一个false

    def run(self):
        LOG.info('开始', time.time())
        self.isRunning = True
        while self.isRunning:
            LOG.info('运行中', time.time())
            threadLock.acquire()
            ret, frame = self.cap.read()  #read()函数表示按帧读取视频，success，frame是read()的两个返回值，
            # ret是布尔值——如果读取帧是正确的则返回True，如果文件读取到结尾则返回False，Frame表示的是每一帧的图像，是一个三维矩阵
            if ret:
                LOG.info('采集到图片', time.time())
                self.out.write(frame)
            threadLock.release()

    def stop(self):
        LOG.info('结束', time.time())
        self.isRunning = False
        self.out.release()


class VideoCamera:
    def __init__(self,cap):
        # 打开摄像头， 0代表笔记本内置摄像头
        self.cap = cap

    def startRecord(self, name):
        self.recordingThread = RecordingThread(name, self.cap)
        self.recordingThread.start()

    def stopRecord(self):
        self.recordingThread.stop()


if __name__ == '__main__':
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)  # 0为本地摄像头，1为外接摄像头
    vv = VideoCamera(cap)
    vv.startRecord('test')
    time.sleep(10)
    vv.stopRecord()