#找到合适的帧率
from cv2.cv2 import VideoCapture, CAP_PROP_FPS, CAP_PROP_FRAME_COUNT, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT


def get_fps(path, recordtime):  # 视频信息
    video = VideoCapture(path)  # 记得文件名加格式不要错！
    old_fps = video.get(CAP_PROP_FPS)
    Count = video.get(CAP_PROP_FRAME_COUNT)
    size = (int(video.get(CAP_PROP_FRAME_WIDTH)), int(video.get(CAP_PROP_FRAME_HEIGHT)))
    print('视频帧率=%.1f' % old_fps)
    print('视频的帧数=%.1f' % Count)
    print('视频的分辨率', size)
    print('视频时间=%.3f秒' % (int(Count) / old_fps))
    print('视频的录制时间=%.3f秒' % recordtime)
    new_fps = old_fps * (int(Count) / old_fps) / recordtime
    print('推荐帧率=%.2f' % (new_fps))

if __name__ == '__main__':
    get_fps(r'D:\zqz\project\dec\photo\finishFigure\videos\20220106_162218.mp4', 4)