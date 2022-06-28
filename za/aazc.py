import numpy as np
import cv2
import time
# 创建一个VideoCapture对象
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# 指定视频编解码方式为MJPG
codec = cv2.VideoWriter_fourcc(*'MJPG')
fps = 20.0 # 指定写入帧率为20
frameSize = (640, 480) # 指定窗口大小
# 创建 VideoWriter对象
out = cv2.VideoWriter('video_record.avi', codec, fps, frameSize)

print("按键Q-结束视频录制")
ss = time.time()
while(cap.isOpened()):

    ret, frame = cap.read()
    # 如果帧获取正常
    if ret==True:
        # 镜像反转 flip
        # frame = cv2.flip(frame, -1)

        # 不断的向视频输出流写入帧图像
        out.write(frame)
        # 在窗口中展示画面
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) == ord('q'):
            ee = time.time()
            break
    else:
        break
print(ee-ss)
# 释放资源
cap.release()
out.release()
cv2.destroyAllWindows()