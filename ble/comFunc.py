from ble.V3common import judgeType
from ble.v2 import processOuterV2, connectcmd
import re
from datetime import datetime

from lib.OtherMethod import resolveflat


class comFunc:
    @staticmethod
    @connectcmd
    @processOuterV2('设置时间')
    def setTime(*args, **kwargs):
        print(args)
        default = datetime.now().strftime('%Y/%m/%d %H:%M')
        print(datetime.now().strftime('%Y/%m/%d %H:%M'))
        args = [default, '8'] if not args else args
        print('aa', args)
        year, month, day, hour, minu = re.findall('(\d{4})/(\d{1,2})/(\d{1,2}) (\d{1,2}):(\d{1,2})', args[0])[0]
        print(year, month, day, hour, minu)
        week = datetime.strptime(year+month+day, '%Y%m%d').weekday()
        cmd = [judgeType(int(year), 4), judgeType(int(month)), judgeType(int(day)), judgeType(int(hour)), judgeType(int(minu)), judgeType(50), judgeType(int(week)), judgeType(0,8), judgeType(args[1], 4)]
        print('cc', cmd)
        cmd = resolveflat(cmd)
        print('as', cmd)
        return cmd

    @staticmethod
    @connectcmd
    @processOuterV2('单位设置')
    def setUnit(*args, **kwargs):
        default = ['km', 'kg', '摄氏度', 90, '英文', '24时制', '周一', '米']
        alldict = {'km': 1, 'mi': 2, 'kg': 1, 'lb': 2, '摄氏度': 1, '华氏度': 2, '中文': 1, '英文': 2, '法语': 3, '德语': 4,
                   '意大利语': 5, '西班牙语': 6, '日语': 7, '波兰语': 8, '捷克语': 9, '罗马尼亚': 10, '立陶苑语': 11,
                   '荷兰语': 12, '斯洛文尼亚语': 13, '匈牙利语': 14, '俄罗斯语': 15, '乌克兰语': 16, '斯洛伐克语': 17,
                   '丹麦语': 18, '克罗地亚语': 19, '印尼语': 20, '韩语': 21, '印地语': 22, '葡萄牙语': 23,
                   '土耳其语': 24, '泰国语': 25, '越南语': 26, '缅甸语': 27, '菲律宾语': 28, '繁体中文': 29,
                   '希腊语': 30, '阿拉伯语': 31, '24时制': 1, '12时制': 2, '周一': 0, '周日': 1, '周六': 2, '米': 1, '码': 2}
        args = [default] if not args else args
        args = [alldict[i] if i in list(alldict) else i for i in args[0]]
        alldata = [args[0], args[1], args[2], args[3], args[4], args[5], args[3], args[3], args[6], args[0],
                   args[7], args[0], args[0]]
        print('all', alldata)
        for i in range(len(alldata)):
            alldata[i] = judgeType(int(alldata[i]), 2)
        alldata = resolveflat(alldata)
        print('as', alldata)
        return alldata

if __name__ == '__main__':
    # hh = ('2022/4/8 17:31', '24')
    # print(re.findall('(\d{4})/(\d{1,2})/(\d{1,2}) (\d{1,2}):(\d{1,2})', '2022/4/11 9:27'))
    import time
    # print(datetime.now().strftime('%Y/%m/%d %H:%M'))
    # comFunc.setTime('2022/4/11 10:38', '8')
    # print(datetime.date(datetime(year=2022, month=4, day=11)))
    # print(datetime.strptime('20220411', '%Y%m%d').weekday())
    # print(datetime.strptime('2022412', '%Y%m%d').weekday())
    print(comFunc.setUnit())
