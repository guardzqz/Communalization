import time
import re

from Logs.log import Loggings

LOG = Loggings()
def judgeType(k, v=2):
    '''
    数字k转16进制，根据v填充位数，位数大于2位要转小端序
    :param k 数值
    :param v 位数
    :return:返回16进制数组
    '''
    if v<=0:
        return None
    if isinstance(k, (int)):
        aa = '{{:0>{}x}}'.format(v).format(k)
    else:
        aa = '{{:0>{}}}'.format(v).format(k)
    if v!=2:
        return [aa[i:i + 2] for i in range(0, len(aa), 2)][::-1]
    return [aa[i:i + 2] for i in range(0, len(aa), 2)][::]

def currentTime(*args):
    '''
    获取当前时间，根据参数返回元组
    :param args: 可选参数，year，mon，mday，hour，min，sec，wday，yday，isdst
    :return:
    '''
    '''可选参数tm_year=2021, tm_mon=12, tm_mday=9, tm_hour=12, tm_min=7, tm_sec=26, tm_wday=3, tm_yday=343, tm_isdst=0'''
    LOG.info('获取当前时间', args)
    localtime = time.localtime(time.time())
    res = []
    for i in args:
        res.append(getattr(localtime, 'tm_'+i))
    return res

def charToAscii(*args):
    '''
    字符，中文转ASCII码
    :param args: 参数1：字符，参数2：可选，长度，字符串长度不足补0
    :return:
    '''
    LOG.info('字符、中文转ASCII码', args)
    res = []
    if args[0]:
        for i in args[0]:
            if len(res)>args[1]:
                return res[:args[1]]
            if '\u4e00' <= i <= '\u9fff':
                for j in i.encode():
                    res.append(hex(j)[2:])
            else:
                res.append(hex(ord(i))[2:])
    if args[1]-len(res)>0:
        res[len(res):args[1]-1]=judgeType(0, (args[1]-len(res))*2)
    return res[:args[1]]


def set_city(city_name):
    pass
    '''设置城市'''
    x = bytes(city_name, "UTF-8")
    city_hex = x.hex()
    city_len_16 = "{:0>2x}".format(int(len(city_hex) / 2))
    cmd = f'{"00" * 10}{city_len_16}{city_hex}'
    cmd = cmd.ljust(172, "0")
    cmd = " ".join(re.findall(r".{2}", cmd))
    return cmd


def splitParas(*args):
    '''以,，分割字符串'''
    LOG.info('用,，分割字符串', args)
    if args[0] and isinstance(args[0], str):
        return re.split('[,，]', args[0])

def repeatDate(*args):
    '''
    根据日期，返回星期打开状态，1为打开，0为关闭
    :param args: dicts中参数
    :return:
    '''
    LOG.info('根据星期，返回状态', args)
    dicts = {
        '不重复':0x0,
        '周一':0x2,
        '周二':0x4,
        '周三':0x8,
        '周四':0x10,
        '周五':0x20,
        '周六':0x40,
        '周日':0x80,
        '工作日':0x3e,
        '每天':0xfe,
    }
    res = 1 if args[0] else 0
    args = args[0] if args[0] else ['不重复']
    for i in args:
        res |= dicts[i]
    return res

def fillList(*args):
    '''
    填充长度为arg[1]的数组arg[0]
    :param args:arg[0]数组 arg[1]需要数组最终的长度
    :return:
    '''
    LOG.info('把数组填充到指定长度', args)
    print(args[0], len(args[0]))
    if len(args[0]) < args[1]:
        args[0][len(args[0]):args[1] - 1] = [0]*(args[1]-len(args[0]))
    print('aa',args[0])
    return args[0]






if __name__ == '__main__':
    print(charToAscii("深圳",10))
    print(set_city("深圳"))