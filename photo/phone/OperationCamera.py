import time

from Logs.log import Loggings
from config.filePath import filePath
from lib.OtherMethod import writeType
from lib.getConfig import getConfig

from lib.yamlMethod import readYaml
from method.OperationDir import writeText
from photo.phone.Phonedriver import Phonedriver
from photo.phone.photoMethod import photoMethod

LOG = Loggings()
class OperationCamera:
    @classmethod
    def camera(cls, path, description=None):
        LOG.info('拍照', path, description)
        d = Phonedriver.getDriver()
        '''执行拍照功能'''
        userdata = readYaml(filePath.USERSARGS)[getConfig('method', 'photo')+'-'+getConfig("user", "photo")]
        wakeupwait = float(userdata["wakeupwait"])  # 获取相机聚焦后等待时间
        Phonedriver.persistApp()
        time.sleep(wakeupwait)
        x_y = (tuple([float(i) for i in userdata['Coordinate'].split(",")]))
        d.click(x_y[0], x_y[1])
        photoMethod.getPhonePicture()
        writeText(filePath.DESCRIPTION, description)
        writeType(path, 'p')



if __name__ == '__main__':
    OperationCamera.camera()

