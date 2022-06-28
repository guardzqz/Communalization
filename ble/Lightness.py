from ble.V3common import judgeType
from ble.v2 import processOuterV2


class Lightness:
    @staticmethod
    @processOuterV2('app设置手表亮度')
    def setLightV2(*args, **kwargs):
        '''
        设置手表亮度等级
        参数1：亮度等级0-100，参数2：显示间隔int型
        '''
        datas = [20, 1, 0, 0, 0, 0, 0, 0, 0, 5]
        args = args[0]
        if len(args)>0:
            datas[0] = int(args[0])
        if len(args)>1:
            datas[9] = int(args[1])
        for i, j in enumerate(datas):
            datas[i] = judgeType(j)
        return datas


if __name__ == '__main__':
    L = Lightness()
    L.setLightV2([10,18])
