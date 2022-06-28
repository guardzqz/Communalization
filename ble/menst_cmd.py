from ble.menstrual import menstrual


class MenstCmd:
    def __init__(self):
        self.c = menstrual()

        pass

    @classmethod
    def menses_his_cmd(cls, menses_his_list):
        '''
        传入一个历史数据列表menses_his_list : [[经期开始日期,经期长度,经期周期],...],
        如:[['2021/12/27', 9, 27], ['2022/1/24', 6, 30], ]
        '''

        cmd = cls().c.historicalMenstruationV3(menses_his_list)
        return cmd

    @classmethod
    def menses_remind_cmd(cls, hour='09:00',start_day=1, ovulation_day=1 ,pregnancy_day_before=1,pregnancy_day_end=1,menstrual_day_end=1):
        '''
        设置提醒参数
        start_day  开始日提醒  提前天数
        ovulation_day 排卵日提醒 提前天数
        hour           提醒时间，形如: '09:00'
        pregnancy_day_before 易孕期 开始的时候 提前多少天提醒
        pregnancy_day_end 易孕期 结束的时候 提前多少天提醒
        menstrual_day_end 经期结束 提前多少天提醒
        '''

        c = menstrual()
        #将/替换为：
        hour = hour.replace('/',':')
        cmd = c.setMenstrualRemindV2([start_day, ovulation_day, hour, pregnancy_day_before, pregnancy_day_end, menstrual_day_end])
        return cmd
    @classmethod
    def menses_set_cmd(cls,on_off,menstrual_lenth,menstrual_cycle,last_menstrual,ovulation_interval_day,ovulation_before_day,ovulation_after_day,notify_flag):
        '''
        经期设置
        经期参数：
            on_off  经期功能开关
            menstrual_lenth 经期天数
            menstrual_cycle 经期周期
            last_menstrual 最后一次经期时间 形如: '2021/12/27'
        设置安全期：
            ovulation_interval_day 设置排卵期在经期前的间隔天数
            ovulation_before_day 安全期在排卵前x天开始
            ovulation_after_day 安全期在排卵后x天结束
        notify_flag  通知方式: ['允许通知', ’静默通知‘，'关闭通知']
        '''


        cmd = cls().c.setMenstrualV2([on_off, menstrual_lenth, menstrual_cycle, last_menstrual,
                                ovulation_interval_day, ovulation_before_day, ovulation_after_day, notify_flag])
        return cmd
    @classmethod
    def ten_to_hex(self, num, several=0):
        """
        num为待转换为16进制数据，
        text为excel单元格中读取到的命令
        serveral 为uint32_t value
        """
        if several == 0:
            several = len(str(num))
            if len(str(num)) % 2 == 1:
                num = "0" + str(num)
                several = len(str(num))
        trans_code = '{:0>{several}x}'.format(int(num), several=several)  # 小端序  several设置位数
        instruct = ''
        for i in range(len(trans_code), 0, -2):
            instruct = "-".join([instruct, trans_code[i - 2:i]])
        return instruct[1:]

    #设置时间
    @classmethod
    def set_time(cls,date):
        '''
        设置时间,格式1: 2021/12/27/09/00'
                格式2: 2021/12/27
        '''
        if len(date) > 11:
            years, months, days, hour, minute,= date.split('/')
            cmd = "03-01-" + cls.ten_to_hex(years) + "-" + cls.ten_to_hex(months) + "-" + cls.ten_to_hex(days) + "-" + cls.ten_to_hex(hour) + "-" + cls.ten_to_hex(minute) + "-38-ff"
        else:
            years, months, days, = date.split('/')
            cmd = "03-01-" + cls.ten_to_hex(years) + "-" + cls.ten_to_hex(months) + "-" + cls.ten_to_hex(days) + "-09-00-38-ff"
        return cmd


if __name__ == '__main__':
    # print(MenstCmd.menses_his_cmd([['2021/12/27', 9, 27], ['2022/1/24', 6, 30]]))
    # print(MenstCmd.menses_remind_cmd(1, 2, '09/00', 2, 3, 1))
    # print(MenstCmd.menses_remind_cmd(0,0,'14/00',0,0,0))

    # print(MenstCmd.menses_set_cmd('开', 7, 30, '2021/6/21', 14, 5, 5, '允许通知'))


    print(MenstCmd.set_time('2022/6/26/20/14'))



