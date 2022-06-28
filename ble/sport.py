# encoding:utf-8
from ble.V3common import judgeType, currentTime, charToAscii, splitParas, repeatDate, fillList
from ble.v3 import processOuterV3
from lib.OtherMethod import resolveflat


class sport:
    @staticmethod
    @processOuterV3('设置运动排列顺序')
    def setSportV3(*args, **kwargs):
        '''
        设置运动排列顺序
    aa = '33-da-ad-da-ad-01-73-00-33-00-88-01-00-02-01-64-'
    bb = '-30-08-31-34-35-16-20-04-32-33-4b-36-37-12-1d-39-38-66-6e-65-3a-68-09-11-0d-25-72-70-0e-73-74-0f-76-75-78-79-7a-7b-7c-7d-7e-7f-80-81-82-83-18-14-19-15-84-07-85-86-87-88-89-8a-1a-8b-8c-8d-24-98-99-9a-06-13-9b-9c-9d-9e-9f-a0-a1-a2-1b-a3-a5-a6-a4-a7-a8-a9-aa-ab-ac-ad-af-b0-ae-b1-b2-b3-b4-b5-b6-b7-b8-76-52'
        '''
        print(args)
        default = {'户外跑步':0x30,'室内跑步':0x31,'户外步行':0x34,'室内步行':0x35,'户外骑行':0x32,'室内骑行':0x33,'泳池游泳':0x36,'开放水域游泳':0x37,
'徒步':0x04,'瑜伽':0x12,'划船机':0x39,'椭圆机':0x38,'板球':0x4B,'健身':0x08,'高强度间歇训练':0x3A,'功能性力量训练':0x65,'核心训练':0x66,
'舞蹈':0x1D,'踏步机':0x67,'整理放松':0x68,'传统力量训练':0x6E,'有氧健身操':0x11,'普拉提':0x20,'仰卧起坐':0x0D,'平板支撑':0x25,
'开合跳':0x72,'引体向上':0x70,'俯卧撑':0x0E,'深蹲':0x73,'高抬腿':0x74,'哑铃':0x0F,'杠铃':0x76,'拳击':0x75,'武术':0x77,'太极':0x78,
'跆拳道':0x79,'空手道':0x7A,'自由搏击':0x7B,'击剑':0x7C,'射箭':0x7D,'体操':0x7E,'单杠':0x7F,'双杠':0x80,'漫步机':0x81,'登山机':0x82,
'保龄球':0x83,'网球':0x18,'乒乓球':0x14,'高尔夫球':0x19,'足球':0x16,'篮球':0x15,'台球':0x84,'羽毛球':0x07,'曲棍球':0x85,
'橄榄球':0x86,'壁球':0x87,'垒球':0x88,'手球':0x89,'毽球':0x8A,'棒球':0x1A,'沙滩足球':0x8B,'藤球':0x8C,'躲避球':0x8D,
'广场舞':0x24,'街舞':0x98,'芭蕾':0x99,'社交舞':0x9a,'登山':0x06,'跳绳':0x13,'飞盘':0x9b,'飞镖':0x9c,'骑马':0x9d,
'爬楼':0x9e,'放风筝':0x9f,'钓鱼':0xa0,'雪橇':0xa1,'雪车':0xa2,'滑冰':0x1b,'单板滑雪':0xa3,'高山滑雪':0xa5,
'越野滑雪':0xa6,'雪上运动':0xa4,'冰壶':0xa7,'冰球':0xa8,'冬季两项':0xa9,'冲浪':0xaa,'帆船':0xab,'帆板':0xac,
'皮艇':0xad,'划艇':0xb8,'赛艇':0xb0,'摩托艇':0xae,'龙舟':0xb1,'水球':0xb2,'漂流':0xb3,'滑板':0xb4,'攀岩':0xb5,'蹦极':0xb6,
'跑酷':0xb7,'bmx':0xb8}
        print('all', len(default))
        args = args[0][0] if args[0] else ['户外跑步','室内跑步','户外步行','室内步行']
        sportlen = len(args)
        data = []
        data.append([1, 2, sportlen, 100])
        for i in args:
            data.append(default[i])
        print(data)
        last = set(list(default))-set(args)
        print(len(last), last)
        for i in last:
            data.append(default[i])
        print(data)
        data = resolveflat(data)
        for i in range(len(data)):
            data[i]=judgeType(data[i])
        return data

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
            i.insert(0, j + 1)
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
    print('-'.join(sport.setSportV3([])))
    # 33 da ad da ad 01 7e 00 41 00 15 00 00 02 09 6f 03 04 0e 10 0a 0b 08 09 05 11 01 1b 17 1c 1d 1e 1f 20 21 23 12 55 06 18 25 5c 5d 27 28 2c 2d 31 32 33 35 36 37 38 39 3a 3b 3d 3f 41 42 5e 5f 44 45 48 49 4c 4e 51 52 53 54 60 57 59 19 02 14 61 62 63 64 65 66 67 68 69 6a 6b 6c 6d 6e 6f 70 71 72 73 74 75 76 77 78 79 7a 7b 7c 7d 7e 7f 80 81 82 83 84 85 86 87 88 89 8a 8b 8c 8d 16 0d 0f 69 76