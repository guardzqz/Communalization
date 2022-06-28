# encoding:utf-8
from ble.V3common import judgeType, currentTime, charToAscii, splitParas, repeatDate, fillList
from ble.v3 import processOuterV3
from lib.OtherMethod import resolveflat


class alarm:
    @staticmethod
    @processOuterV3('App获取闹钟列表')
    def getAlarmV3(*args, **kwargs):
        '''
        获取ble闹钟数据
        :param args: arg[0] 获取闹钟标志
        '''
        datas = 0x0
        if args:
            datas = args[0]
        datas = judgeType(datas)
        return datas

    @staticmethod
    @processOuterV3('app设置ble的V3闹钟')
    def setAlarmV3(*args, **kwargs):
        '''
        V3闹钟一共有10个数组
        :param args: 参数1：显不显示，参数2：类型，参数3：时，参数4：分钟，参数5：重复日期，参数6：贪睡时长，参数7：延时分钟，参数8：震动开关，参数9：重复闹铃次数，参数10：闹钟名称
        :param kwargs:
        :return:
        '''
        args = args[0]
        max_alarm_num = 10
        max_name_len = 24
        defaults = ['不显示', '起床', currentTime('hour')[0], currentTime('min')[0], '每天', 0x0, 0x0, 0x0, 0x0, None]
        dicts = {'status': {'显示': 0x55, '不显示': 0xaa},
                 'type': {'起床': 0x00, '睡觉': 0x01, '锻炼': 0x02, '吃药': 0x03, '约会': 0x04, '聚会': 0x05, '会议': 0x06,
                          '其他': 0x07}}
        alldata = []
        for j in range(max_alarm_num):
            '''每个闹钟长度补足0'''
            if len(args) <= j:
                i = fillList([], 10)
            else:
                i = fillList(args[j], 10)
            '''每个闹钟没有配置的取默认配置，特殊处理参数'''
            i = [i[j] if i[j] else defaults[j] for j in range(len(defaults))]
            '''闹钟显示，类型，重复日期'''
            i[0], i[1], i[4] = dicts['status'][i[0]], dicts['type'][i[1]], repeatDate(splitParas(i[4]))
            '''闹钟名称'''
            if not isinstance(i[9], (list)):
                i[9] = charToAscii(i[9], max_name_len)
            '''每个闹钟前加序号'''
            i.insert(0, j+1)
            alldata.append(i)
        '''整体协议补充，展开，转16进制'''
        alldata.insert(0, [0, 10])
        alldata = resolveflat(alldata)
        for j in range(len(alldata)):
            alldata[j] = judgeType(alldata[j])[0]
        return alldata



if __name__ == '__main__':
    # print(hasattr(alarm, 'getAlarmV3'))
    # alarm.getAlarmV3()
    # alarm.getAlarmV3(0)
    # alarm.setAlarmV3((['显示', '锻炼', 12, 1, '周一，周二'], ['不显示', '会议',2021, 12, 0, 0, 0, 0, 0,'jihuf'],['不显示', '会议',2021, 12, 0, 0, 0, 0, 0,'jihuf'],['不显示', '会议',2021, 12, 0, 0, 0, 0, 0,'jihuf'],['不显示', '会议',2021, 12, 0, 0, 0, 0, 0,'jihuf'],['不显示', '会议',2021, 12, 0, 0, 0, 0, 0,'jihuf'],['不显示', '会议',2021, 12, 0, 0, 0, 0, 0,'jihuf'], ['显示', '锻炼', 12, 1, '周一，周二'], ['不显示', '会议',2021, 12, 0, 0, 0, 0, 0,'jihuf'],['不显示', '会议',2021, 12, 0, 0, 0, 0, 0,'jihuf'],['不显示', '会议',2021, 12, 0, 0, 0, 0, 0,'jihuf'],['不显示', '会议',2021, 12, 0, 0, 0, 0, 0,'jihuf'],['不显示', '会议',2021, 12, 0, 0, 0, 0, 0,'jihuf'],['不显示', '会议',2021, 12, 0, 0, 0, 0, 0,'jihuf']))
    alarm.setAlarmV3((['显示', '起床',1, 1, '周三'],))