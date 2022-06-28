import os
import subprocess
import time

import cv2
import numpy as np
from PIL import Image

from Logs.log import Loggings
from config.filePath import filePath
from lib.getConfig import getConfig

from lib.yamlMethod import readYaml

LOG = Loggings()
class photoMethod:
    @classmethod
    def getPhonePicture(cls):
        '''
        获取时间最近的一张手机照片
        '''
        LOG.info('获取图片')
        pic = ['']
        pathRoute = readYaml(filePath.USERSARGS)[getConfig('method', 'photo')+'-'+getConfig("user", "photo")]['CameraPhoto']
        while pic == ['']:
            time.sleep(1)
            p = subprocess.Popen('adb -s {} shell ls -t {}'.format(getConfig("camera", "photo"), pathRoute), stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, stdin=subprocess.DEVNULL)
            pic = p.stdout.read().decode(encoding='utf-8').split("\r\n")
        subprocess.Popen('adb -s {} pull {}/{} {} '.format(getConfig("camera", "photo"), pathRoute, pic[0], filePath.OPICTURES_DIR),
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL)
        time.sleep(0.5)
        photoMethod.screenshot()
        '''读完图片之后会删除图片，否则手机有图片，找到的可能不是最新的'''
        photoMethod.delphonePicture()

    @classmethod
    def delphonePicture(cls):
        '''
        删除手机照片
        '''
        LOG.info('删除图片')
        pathRoute = readYaml(filePath.USERSARGS)[getConfig('method', 'photo')+'-'+getConfig("user", "photo")]['CameraPhoto']
        subprocess.Popen('adb -s {} shell cd {}&&rm -rf ./*'.format(getConfig("camera", "photo"), pathRoute), stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, stdin=subprocess.DEVNULL)

    @classmethod
    def screenshot(cls):
        '''
        打开一张图，并截图区域，按比例改变尺寸，旋转
        '''
        LOG.info('打开一张图，并截图区域，按比例改变尺寸，旋转')
        lists = os.listdir(filePath.OPICTURES_DIR)
        lists.sort(key=lambda x: os.path.getatime((filePath.OPICTURES_DIR + os.sep + x)))
        userdata = readYaml(filePath.USERSARGS)[getConfig('method', 'photo')+'-'+getConfig("user", "photo")]
        img = Image.open(os.path.join(filePath.OPICTURES_DIR, lists[-1]))
        size = tuple([int(i) for i in userdata["Screenshot"].strip("()").split(",")])
        region = img.crop(size)
        region = cls.reSizeImage(region, userdata['ratio'])
        # w, h = region.size
        # region = region.resize((int(w * float(userdata["ratio"])), int(h * float(userdata["ratio"]))))

        region.save(os.path.join(filePath.FPICTURES_DIR, lists[-1]))
        photoMethod.rotateImage(os.path.join(filePath.FPICTURES_DIR, lists[-1]), userdata['rotation_angle'])

    @classmethod
    def ImageRatio(cls, path):
        region = Image.open(os.path.join(filePath.OPICTURES_DIR, path))
        region = cls.reSizeImage(region, readYaml(filePath.USERSARGS)[getConfig('method', 'photo')+'-'+getConfig("user", "photo")]['ratio'])
        region.save(os.path.join(filePath.FPICTURES_DIR, path))

    @classmethod
    def reSizeImage(cls, region, ratio):
        '''按比例改变图片尺寸'''
        w, h = region.size
        region = region.resize((int(w * float(ratio)), int(h * float(ratio))))
        return region


    '''顺时针旋转'''
    @classmethod
    def rotateImage(cls, path, angle=90):
        LOG.info('旋转图片', path)
        img = cv2.imread(path)
        img_rotate = photoMethod.rotateBound(img, int(angle))
        cv2.imwrite(path, img_rotate)

    @classmethod
    def rotateBound(cls, image, angle):
        (h, w) = image.shape[:2]
        (cX, cY) = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])
        # compute the new bounding dimensions of the image
        nW = int((h * sin) + (w * cos))
        nH = int((h * cos) + (w * sin))
        # adjust the rotation matrix to take into account translation
        M[0, 2] += (nW / 2) - cX
        M[1, 2] += (nH / 2) - cY
        # perform the actual rotation and return the image
        return cv2.warpAffine(image, M, (nW, nH))

if __name__ == '__main__':
    photoMethod.getPhonePicture()

