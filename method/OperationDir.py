import os
import shutil
from datetime import datetime
from zipfile import ZIP_DEFLATED, ZipFile

from Logs.log import Loggings
from config.filePath import filePath
from lib.getConfig import getConfig

from photo.phone.photoMethod import photoMethod

LOG = Loggings()
def writeText(path, data=None):
    '''
    写入数据到文件txt
    :param path:
    :param data:1.new新建文件 2.None占位写到文件 3.有数据直接写到文件
    :return:
    '''
    if data is 'new':
        with open(path, 'w', encoding='utf-8') as f:
            LOG.info('新建文件'+path)
            return
    with open(path, 'a+', encoding='utf-8') as f:
        if data is None:
            data = ''
        f.write(data+'\n')
        LOG.info('写入文件'+path+':数据'+data)

def clearStatus():
    '''清理之前的现场'''
    LOG.info('跑脚本前清理现场')
    if getConfig('method', 'photo') == 'phone':
        photoMethod.delphonePicture()
    delDir()
    writeText(filePath.DESCRIPTION, 'new')

def aZip():
    '''备份图片视频'''
    dest = filePath.ZIPSTORAGE_DIR + os.sep + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.zip'
    LOG.info('备份图片视频', dest)
    src = filePath.OSOURCES_DIR
    with ZipFile(dest, 'w', ZIP_DEFLATED) as f:
        for dirpath, dirnames, filenames in os.walk(src):
            fpath = dirpath.replace(src, '')  # 这一句很重要，不replace的话，就从根目录开始复制
            fpath = fpath and fpath + os.sep or ''  # 这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
            for filename in filenames:
                f.write(os.path.join(dirpath, filename), fpath + filename)
        LOG.info(dest, '压缩成功')

def delOmk(dirpath):
    """删除目录下的文件"""
    LOG.info(f"删除{dirpath}")
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    for path, dirnames, filenames in os.walk(dirpath):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行删除
        fpath = path.replace(dirpath, '')
        for filename in filenames:
            # 获取该文件下所有的子文件绝对路径
            dir, document = os.path.join(path, filename), os.path.join(fpath, filename)
            # 删除文件
            os.remove(dir)

def delDir(paths=None):
    LOG.info('文件操作', paths)
    if paths==None:
        # paths = [filePath.OPICTURES_DIR, filePath.FPICTURES_DIR, filePath.OVIDEOS_DIR, filePath.FVIDEOS_DIR]
        paths = [filePath.OPICTURES_DIR, filePath.FPICTURES_DIR, filePath.OVIDEOS_DIR]
    for i in paths:
        delOmk(i)

def getPicYield(destpath, path = filePath.FPICTURES_DIR):
    LOG.info('读取资源文件并拷贝一份到新地址', path, destpath)
    if not os.path.exists(destpath):
        os.makedirs(destpath)
    for i in os.listdir(path):
        shutil.copy(os.path.join(path, i), os.path.join(destpath, i))
        yield os.path.join(destpath, i)

def getDescriptionYeild(path=filePath.DESCRIPTION):
    LOG.info('读取拍照说明', path)
    with open(path, 'r', encoding='utf-8') as f:
        for i in f.readlines():
            yield i

if __name__ == '__main__':
    # writeText(filePath.DESCRIPTION,'new')
    # writeText(filePath.DESCRIPTION)
    # writeText(filePath.DESCRIPTION,'aa')
    # writeText(filePath.DESCRIPTION)
    # delDir()
    # hh = getPicYield(r'D:\zqz\project\dec\result\alarm\2021-12-27-10-21-40\pictures')
    # print(hh.__next__())
    # print(hh.__next__())
    # print(hh.__next__())
    # print(hh.__next__())
    with open(r'D:\zqz\project\dec\TEXT/拍照序列.txt', 'r', encoding='utf-8') as f:
        print(f.readlines())
