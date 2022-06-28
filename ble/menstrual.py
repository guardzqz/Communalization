'''
### 3.34 经期设置

**命令字和key**：（command\_id为0x03， key为 0x41）

**功能描述**

手机app通过这个命令通知手环经期设置

**1）app发送经期设置**

```c
//设置经期
struct protocol_set_menstrual
{
    struct protocol_head head;
    uint8_t on_off;             //开关 0xAA开,0x55关闭
    uint8_t menstrual_length;  //经期长度
    uint8_t menstrual_cycle;    //经期周期
    uint16_t last_menstrual_year; //最近一次经期开始时间
    uint8_t last_menstrual_month;
    uint8_t last_menstrual_day;    //

    //以下用于 app 修正计算公式
    uint8_t ovulation_interval_day;    //从下一个经期开始前到排卵日的间隔,一般为14天
    uint8_t ovulation_before_day;  //排卵日之前易孕期的天数,一般为5,
    uint8_t ovulation_after_day;   //排卵日之后易孕期的天数,一般为5,
    uint8_t notify_flag;//通知类型 ： 0无效 ； 1：允许通知； 2：静默通知； 3：关闭通知    bool menstrual_add_notify_flag_03_41;// 生理周期开关增加通知类型
};
```

| 1Byte                                                        | 1Byte                                                        | 1Byte                                                        |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| on_off<br />开关<br />0xAA开,0x55关闭                        | menstrual_length<br />经期长度<br />单位天                   | menstrual_cycle<br />经期周期<br />单位天                    |
| 2Bytes                                                       | 1Byte                                                        | 1Byte                                                        |
| last_menstrual_year<br />上一次经期开始时间<br />年          | last_menstrual_month<br />月                                 | last_menstrual_day<br />日                                   |
| 1Byte                                                        | 1Byte                                                        | 1Byte                                                        |
| ovulation_interval_day<br />从下一个经期开始前到排卵日的间隔<br />从下一个经期开始前倒数天数，一般为14天 | ovulation_before_day<br />排卵日之前易孕期的天数<br />一般为5天 | ovulation_after_day<br />排卵日之后易孕期的天数<br />一般为5天 |
| 9Bytes                                                       |                                                              |                                                              |
| reserved<br/>预留：全部补0                                   |                                                              |                                                              |

**2）ble设备回复经期设置**

| 18Bytes                    |
| -------------------------- |
| reserved<br/>预留：全部补0 |
'''
from ble.V3common import fillList, judgeType
from ble.v2 import processOuterV2, connectcmd
from datetime import datetime

from ble.v3 import processOuterV3
from lib.OtherMethod import resolveflat
import re


class menstrual:
    @staticmethod
    def getNowTime(name):
        return str(getattr(datetime.today(), name))

    @staticmethod
    @connectcmd
    @processOuterV2('经期设置')
    def setMenstrualV2(*args, **kwargs):
        '''
        经期设置
        参数：
        on_off = {'开':'aa', '关':'55'}
        menstrual_lenth = 7
        menstrual_cycle = 30
        last_menstrual_year = Women.getNowTime('year')
        last_menstrual_month = Women.getNowTime('month')
        last_menstrual_day = Women.getNowTime('day')
        ovulation_interval_day = 14
        ovulation_before_day = 5
        ovulation_after_day = 5
        notify_flag = 1
        '''
        pass
        defaultData = ['开', 7, 30, menstrual.getNowTime('year')+'/'+menstrual.getNowTime('month')+'/'+
                       menstrual.getNowTime('day'), 14, 5, 4, '允许通知']
        on_off = {'开':170, '关':85}
        notify = {'允许通知':1, '静默通知':2, '关闭通知':3}
        args = fillList(list(args[0]), 8)
        # 如果没有传入参数则用默认值
        lastdata = [args[i] if args[i] else defaultData[i] for i in range(len(args))][:8]
        lastdata[0] = on_off[lastdata[0]]
        lastdata[3] = [int(i) for i in re.findall('(\d{4})/(\d{1,2})/(\d{1,2})', lastdata[3])[0]]
        lastdata[-1] = notify[lastdata[-1]]
        lastdata = resolveflat(lastdata)
        lastcmd = []
        for i in range(len(lastdata)):
            if i==3:
                lastcmd.append(judgeType(lastdata[i], 4))
                continue
            lastcmd.append(judgeType(int(lastdata[i]), 2))
        lastcmd = resolveflat(lastcmd)
        return lastcmd



    '''
### 3.35 经期提醒设置

**命令字和key**：（command\_id为0x03， key为 0x42）

**功能描述**

手机app通过这个命令通知手环经期提醒设置

**1）app发送经期提醒设置**

```c
//设置经期提醒
struct protocol_set_menstrual_remind
{
    struct protocol_head head;
    uint8_t start_day;  //开始日提醒  提前天数
    uint8_t ovulation_day; //排卵日提醒 提前天数
    uint8_t hour;           //提醒时间
    uint8_t minute;
        // bool v2_03_42_menstrual_remind_02_add_pregnancy; //v2经期提醒设置 增加易孕期和结束时间设置
    uint8_t pregnancy_day_before_remind; //易孕期 开始的时候 提前多少天提醒
    uint8_t pregnancy_day_end_remind; //易孕期 结束的时候 提前多少天提醒
    uint8_t menstrual_day_end_remind; //经期结束 提前多少天提醒
};
```

| 1Byte                                                        | 1Byte                                                        | 1Byte                                                        |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| start_day<br />开始日提醒  提前天数                          | ovulation_day<br />排卵日提醒 提前天数                       | hour<br />提醒时间 的时                                      |
| **1Bytes**                                                   | **1Bytes**                                                   | **1Bytes**                                                   |
| minute<br />提醒时间 的分                                    | pregnancy_day_before_remind<br/><br />易孕期 开始的时候 提前多少天提醒 <br />单位天 | pregnancy_day_end_remind<br />易孕期 结束的时候 提前多少天提醒<br />单位 天 |
| **1Bytes**                                                   | **11Bytes**                                                  |                                                              |
| menstrual_day_end_remind<br />经期结束 提前多少天提醒<br />单位 天 | 预留<br />默认是0                                            |                                                              |

**周期变化**

月经期->(安全期)->易孕期(排卵日)->安全期->

假设某一个用户经期开始日志为1-1日，经期长度为5天，周期为28天

**具体计算方案以产品经理为准**



**美柚的一些计算方案**

无论经期或者周期为多久，排卵日计算，为下一个经期前的14天

经期前的安全期：排卵后5天，5天内为易孕期

经期后的安全期，排卵期5天，5天内为易孕期

经期为开始时间+ 经期长度

其余时间为安全期，

经期后的安全期计算，排卵日前5天为易孕期，如果经期持续时间覆盖了易孕期，则没有安全期
'''

    @staticmethod
    @connectcmd
    @processOuterV2('经期提醒设置')
    def setMenstrualRemindV2(*args):
        pass
        '''
         uint8_t start_day;  //开始日提醒  提前天数
            uint8_t ovulation_day; //排卵日提醒 提前天数
            uint8_t hour;           //提醒时间
            uint8_t minute;
                // bool v2_03_42_menstrual_remind_02_add_pregnancy; //v2经期提醒设置 增加易孕期和结束时间设置
            uint8_t pregnancy_day_before_remind; //易孕期 开始的时候 提前多少天提醒
            uint8_t pregnancy_day_end_remind; //易孕期 结束的时候 提前多少天提醒
            uint8_t menstrual_day_end_remind; //经期结束 提前多少天提醒
        '''
        defaultData = [1, 2, '20:00', 3, 3, 3]
        args = fillList(args[0], 6)
        lastcmd = []
        lastdata = [args[i] if args[i] else defaultData[i] for i in range(len(args))]
        lastdata[2] = list(re.findall('(\d{1,2}):(\d{1,2})', lastdata[2])[0])
        lastdata = resolveflat(lastdata)
        for i in range(len(lastdata)):
            lastcmd.append(judgeType(int(lastdata[i]), 2))
        lastcmd = resolveflat(lastcmd)
        return lastcmd

    '''
    ### 15.19.经期的历史数据下发

**命令字和key：**(cmd = 0x33,cmd_id = 0x3D)

**说明：**收到的需求是固件要显示5次的历史经期数据，app这边根据数据库查询，然后将所有的数据下发给固件端显示

固件显示的数据包括：开始时间（年月日），经期长度，周期长度，平均经期长度，平均周期长度

**功能表：**

```c
// bool v3_33_3D_historical_menstruation_01_create; //v3经期的历史数据下发
```

app发送

```c
cmd = 0x33;
//头部定义
typedef struct protocol_v3_base
{
	uint32_t fixed;
	uint8_t version;
	uint16_t length;
	uint16_t cmd_id; 
	uint16_t nseq;
}protocol_v3_base_s;

// bool v3_33_3D_historical_menstruation_01_create; //v3经期的历史数据下发
#define MAX_HISTORICAL_MENTRUATION_ITEM_SIZE (5)
//顺序是按照历史的排序到当前的，按照时间点排序设置
//item0是时间最早的，item5是时间最近的，也就是当前的
struct protocol_v3_historical_menstruation_item
{
    uint16_t year; //经期开始的年
    uint8_t mon; //经期开始的月
    uint8_t day; //经期开始的天
    uint8_t menstrual_day; //经期长度 单位天
    uint8_t cycle_day; //周期长度 单位天
};
struct protocol_v3_historical_menstruation
{
    uint8_t version;         //1开始
    uint8_t avg_menstrual_day; //平均经期长度
    uint8_t avg_cycle_day;     //平均周期长度c

    uint8_t items_len; //个数
    struct protocol_v3_historical_menstruation_item items[MAX_HISTORICAL_MENTRUATION_ITEM_SIZE];
};
```

'''

    @staticmethod
    @connectcmd
    @processOuterV3('经期的历史数据下发')
    def historicalMenstruationV3(*args):
        pass
        defaultset = [menstrual.getNowTime('year')+'/'+menstrual.getNowTime('month')+'/'+
                       menstrual.getNowTime('day'), 7, 30]
        args = [defaultset] if not args[0] else args[0]
        for i in range(len(args)):
            args[i][0] = list(re.findall('(\d{4})/(\d{1,2})/(\d{1,2})', args[i][0])[0])
            args[i] = resolveflat(args[i])
            for j in range(len(args[i])):
                args[i][j] = int(args[i][j])
        menlen = 0
        cirlen = 0
        itemlen = len(args)
        for i in range(itemlen):
            menlen += args[i][3]
            cirlen += args[i][4]
            args[i][0] = judgeType(args[i][0], 4)
            for j in range(1, 5):
                args[i][j] = judgeType(args[i][j])
        menlen = round(menlen/itemlen)
        cirlen = round(cirlen/itemlen)
        lastcmd = ['01', judgeType(menlen), judgeType(cirlen), judgeType(itemlen), args]
        lastcmd = resolveflat(lastcmd)
        return lastcmd



if __name__ == '__main__':
    # from datetime import datetime
    # print(datetime.now())
    # print(datetime.today().year, datetime.today().month, datetime.today().day)
    # print(Women().getNowTime('year'))
    # print(menstrual.setMenstrualV2(['开', 7, 30, 2022, 4, 5, 6, 7, 8, 9]))
    # print(menstrual.setMenstrualV2(['开']))
    # print(menstrual.setMenstrualV2(['关']))
    # # print([int(i) for i in re.findall('(\d{4})/(\d{1,2})/(\d{1,2})', '2022/4/11')[0]])
    # print(menstrual.setMenstrualRemindV2([3, 3, '19:00', 2, 3, 3]))
    # print(menstrual.setMenstrualRemindV2([]))
    # print(menstrual.setMenstrualRemindV2([1, 2, 9, 2, 2, 2]))
    # print(menstrual.historicalMenstruationV3([[2021, 2, 1, 7, 27], [2021, 1, 3, 5, 30],  [2021, 9, 1, 7, 30], [2021, 1, 1, 7, 30]]))
    # print(menstrual.historicalMenstruationV3([]))

    test_calss = menstrual()

    print(test_calss.setMenstrualV2(['开', 10, 40]))

    print(test_calss.historicalMenstruationV3([['2021/12/27', 9, 27],['2022/1/24', 6, 30],['2022/2/24', 6, 30],['2022/3/24', 7, 30],['2022/4/24', 8, 31]]))

    print(test_calss.setMenstrualRemindV2([1, 3, '12:20', 2, 3, 3]))


    # print(list(re.findall('(\d{4})/(\d{1,2})/(\d{1,2})', '2022/4/11')[0]))
    # print(re.findall('(\d{4})/(\d{1,2})/(\d{1,2})', '2022/4/11')[0])