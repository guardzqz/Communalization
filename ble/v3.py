from Logs.log import Loggings
from ble.V3common import judgeType
from config.filePath import filePath
from lib.OtherMethod import resolveflat

from lib.yamlMethod import readYaml

LOG = Loggings()
def V3ProBase(*args, **kwargs):
    '''
    处理v3协议头：到yaml获取cmd_id
    :param args[0]: 所有数据，args[1]: 函数中文名称
    '''
    LOG.info('处理v3协议头', args, kwargs)
    base = ['33', 'da', 'ad', 'da', 'ad', '01', '00', '00', '00', '00', 'b1', '00']
    base[8:10] = judgeType(readYaml(filePath.bleExplain)[kwargs['funcname']]['cmd_id'], 4)
    try:
        # 数据长度加11（v3协议头）
        base[6:8] = judgeType(len(kwargs['dataslen'])+11, 4)
    except Exception as e:
        LOG.exception('传参错误', e)
    return base



def V3AllCmd(*args, **kwargs):
    '''组合协议头，数据，检验码生成最后协议
    :param args[0] 协议头 arg[1] 数据
    '''
    LOG.info('组合协议头', args)
    args = resolveflat(args)
    crc = cal_crc(args[1:])
    args.extend(crc)
    return sendByMtu(args)


def cal_crc(pdata):
    '''根据数据生成检验码，数据为十进制类型'''
    crc = 0xFFFF
    for i in pdata:
        crc = ((crc >> 8) | (crc << 8)) & 0xFFFF
        crc = crc ^ int(i, 16)
        crc = (((crc & 0xFF) & 0xFFFF) >> 4) ^ crc
        crc = (crc ^ ((crc << 8) << 4) & 0xFFFF)
        crc = crc ^ (((crc & 0xFF) << 4) << 1 & 0xFFFF)
    return judgeType(crc, 4)

def sendByMtu(datas):
    '''
    根据手表mtu长度发送数据，从第二个序列开始要在数据段前加33
    :param datas:
    :return:
    '''
    LOG.info('根据手环mtu长度发送',datas)
    permissLen = readYaml(filePath.wristPara)['mtu']
    alldata = datas
    templen = 0
    if len(datas)>permissLen:
        alldata = []
        alldata.append(datas[:permissLen])
        datas= datas[permissLen:]
        while len(datas)>0:
            alldata.append(datas[:permissLen-1])
            templen += 1
            alldata[templen].insert(0, '33')
            datas = datas[templen*permissLen - templen:]
    return alldata


def processOuterV3(*args):
    '''
    处理v3协议头和获取最后生成的协议
    :param args: arg[0]函数中文名称
    :return:
    '''
    funcname = args[0]
    def outer(func):
        def inter(*args, **kwargs):
            alldata = func(*args, **kwargs)
            base = V3ProBase(dataslen=alldata, funcname=funcname)
            res = V3AllCmd(base, alldata)
            LOG.info('最终协议', res)
            return res
        return inter
    return outer

if __name__ == '__main__':
    pass
    sendByMtu(['33', 'da', 'ad', 'da', 'ad', '01', '61', '01', '0e', '00', 'b1', '00', '00', '0a', '00', '55', '02', '0c', '01', '03', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '01', 'aa', '06', '7e', '0c', '7f', '00', '00', '00', '00', '6a', '69', '68', '75', '66', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '02', '55', '00', '10', '11', '7f', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '03', '55', '00', '10', '11', '7f', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '04', '55', '00', '10', '11', '7f', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '05', '55', '00', '10', '11', '7f', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '06', '55', '00', '10', '11', '7f', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '07', '55', '00', '10', '11', '7f', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '08', '55', '00', '10', '11', '7f', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '09', '55', '00', '10', '11', '7f', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', 'aa', '0a'])
