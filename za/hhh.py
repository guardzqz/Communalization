from PIL import ImageGrab
import numpy as np
import cv2
from cv2 import VideoCapture, CAP_PROP_FPS, CAP_PROP_FRAME_COUNT, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT
import datetime
import time
import os

import threading

from za.ReadConf import ReadConf

conf = ReadConf()


class ScreenVideoControl(threading.Thread):
    def __init__(self, save_dir):
        threading.Thread.__init__(self)
        self.fps = int(conf.get_value('conf', 'fps'))  # 帧率为25，可以调节
        self.start_time = time.time()
        self.save_dir = save_dir
        self.screen_file_path = None
        self.get_video_path()
        self.video = cv2.VideoWriter(self.screen_file_path, cv2.VideoWriter_fourcc(*'XVID'), self.fps,
                                     ImageGrab.grab().size)

    def start(self):
        # 设置运行开始标志 FLAG=true则为结束录频
        conf.write_or_update_value('conf', "FLAG", 'False')
        # 最长录制时间
        time_delay = 10.0  # 秒 可设置
        self.video_record(time_delay)

    def video_record(self, time_delay):
        print("screen record is doing........")
        print('---录屏已经开始了--')
        while True:
            im = ImageGrab.grab()
            imm = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)  # 转为opencv的BGR格式
            self.video.write(imm)
            self.now_time = time.time()
            delay = self.now_time - self.start_time
            if delay >= time_delay:
                print("---超过指定时间，录制结束！---")
                break
            elif self.end_process():
                print("---程序结束，录制结束！---")
                break
        self.video.release()
        cv2.destroyAllWindows()

    # 判断是否结束
    def end_process(self):
        flag = conf.get_value("conf", 'FLAG')
        if flag == 'False' or flag == "false":
            return False
        else:
            return True

    def get_video_path(self):
        # 录屏保存的文件目录路径
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        # 得到录屏保存的文件路径 按照时间创建文件夹
        file_name = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S') + '_screen.avi'
        # 文件路径
        self.screen_file_path = os.path.join(self.save_dir, file_name)

    #找到合适的帧率
    def get_fps(self):  # 视频信息
        video = VideoCapture(self.screen_file_path)  # 记得文件名加格式不要错！
        old_fps = video.get(CAP_PROP_FPS)
        Count = video.get(CAP_PROP_FRAME_COUNT)
        size = (int(video.get(CAP_PROP_FRAME_WIDTH)), int(video.get(CAP_PROP_FRAME_HEIGHT)))
        print('视频帧率=%.1f' % old_fps)
        print('视频的帧数=%.1f' % Count)
        print('视频的分辨率', size)
        print('视频时间=%.3f秒' % (int(Count) / old_fps))
        print('视频的录制时间=%.3f秒' % (self.now_time - self.start_time))
        new_fps = old_fps * (int(Count) / old_fps) / (self.now_time - self.start_time)
        print('推荐帧率=%.2f' % (new_fps))
        # 把调整过的帧率四舍五入写入配置文件中，下次录制直接拿取
        conf.write_or_update_value('conf', "fps", str(round(float(new_fps))))


if __name__ == "__main__":
    path = r'D:\zqz\project\dec\za'
    t1 = ScreenVideoControl(path)
    t1.start()
    time.sleep(1)  # 等待视频释放过后
    t1.get_fps()