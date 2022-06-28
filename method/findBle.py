import socket
import re
import time

from Logs.log import Loggings
from ble.alarm import alarm
from ble.Lightness import Lightness
from ble.sport import sport
from config.filePath import filePath

from lib.getConfig import getConfig

from lib.yamlMethod import readYaml
LOG = Loggings()
class findBle:
    '''根据名称查找蓝牙协议并发送数据给服务器端'''
    _instance = None
    _ins = False

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            LOG.info('调了ble客户端')
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._ins:
            self._ins = True
            LOG.info('开启手表通信')
            ip_port = (getConfig('ip', 'host'), int(getConfig('port', 'host')))
            self.s = socket.socket()  # 创建套接字
            self.s.connect(ip_port)  # 连接服务器


    @classmethod
    def sendData(cls, data):
        '''发送数据给服务器端'''
        LOG.info('发送消息', data)
        if not data:  # 防止输入空信息，导致异常退出
            return
        cls().s.sendall(data.encode())
        if data == "exit":  # 如果输入的是‘exit’，表示断开连接
            LOG.info("结束通信！")
            findBle.endSocket()
        else:
            server_reply = cls().s.recv(1024).decode()
            LOG.info("回复", server_reply)

    @classmethod
    def endSocket(cls):
        LOG.info('关闭连接')
        cls().s.close()  # 关闭连接

    @classmethod
    def judgeName(cls, *args, **kwargs):
        '''根据名称查找蓝牙协议'''
        LOG.info('根据名称查找蓝牙协议', args)
        if args[0] == 'exit':
            return
        place = readYaml(filePath.bleExplain)[args[0]]['function']
        place = re.split('-', place)
        if len(place)==2 and hasattr(eval(place[0]), place[1]):
            f = getattr(eval(place[0]), place[1])
            if len(args)>1:
                res = f(args[1:])
            else:
                res = f()
            if isinstance(res[0], list):
                for i in res:
                    findBle.sendData(''.join(i))
            else:
                findBle.sendData(''.join(res))
        else:
            LOG.exception('找不函数', args[0])
            raise Exception('找不到这个函数', args[0])


if __name__ == '__main__':
    d = findBle()
    d = findBle()
    d.judgeName('App获取闹钟列表')
    time.sleep(11)
    d.judgeName('app设置ble的V3闹钟', ['不显示', '会议',2021, 12, 0, 0, 0, 0, 0,'jihuf'])
    d.judgeName('app设置ble的V3闹钟', ['不显示', '会议',2021, 12, 0, 0, 0, 0, 0,'jihuf'], ['显示', '会议',2021, 12, 0, 0])
    d.judgeName('exit')
    print('zaidengyixia')
    time.sleep(10)
