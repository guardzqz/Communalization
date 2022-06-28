import socket
import time

from Logs.log import Loggings
from config.filePath import filePath
from lib.OtherMethod import writeType
from method.OperationDir import writeText

LOG = Loggings()
class usbClient:
    _instance = None
    _single = False

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            LOG.info('调了一个usb相机实例')
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        '''
        连接服务端
        :return:
        '''
        if not self._single:
            LOG.info('连接usb server ("127.1.1.1", 1998)')
            self._single = True
            self.sk_con = socket.socket()
            self.sk_con.connect(("127.1.1.1", 1998))

    @classmethod
    def controlUsb(cls, *data):
        '''发送数据给服务器端'''
        LOG.info('发送消息', data)
        if not data:  # 防止输入空信息，导致异常退出
            return
        cls().sk_con.sendall(data[0].encode())
        if data[0] == "q":  # 如果输入的是‘exit’，表示断开连接
            cls().endSocket()
            return
        if data[0] == 'p':
            writeType(data[1], 'p')
        elif data[0] == 'e':
            writeType(data[1], 's')
        if len(data) == 3:
            writeText(filePath.DESCRIPTION, data[2])

    @classmethod
    def endSocket(cls):
        LOG.info('关闭usb连接')
        cls().sk_con.close()


if __name__ == '__main__':
    client=usbClient()
    while True:
        client.controlUsb("p", r'D:\zqz\project\dec\config\caseTemp\alarm.yaml', 'hhh')
        time.sleep(2)
        client.controlUsb("p", r'D:\zqz\project\dec\config\caseTemp\alarm.yaml', 'hhh')
        time.sleep(2)
        client.controlUsb("p", r'D:\zqz\project\dec\config\caseTemp\alarm.yaml', 'hhh')
        time.sleep(2)
        client.controlUsb("s")
        time.sleep(15)
        client.controlUsb("e", r'D:\zqz\project\dec\config\caseTemp\alarm.yaml','hhhff')
        time.sleep(2)
        # client.controlUsb("exit")
        break
    # client.sendData("s")
    # client.sendData("s")
    # client.sendData("s")
    # client.sendData("s")
    # client.sendData("exit")
    # print("0k")
    # pass

