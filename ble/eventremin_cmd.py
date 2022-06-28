import re
import sys

from config.filePath import filePath
from lib.yamlMethod import readYaml

class eventCmd:
    event_list = []
    def __init__(self):
        pass
    @classmethod
    def cal_crc(cls,pdata):
        crc = 0xFFFF
        for i in pdata:
            crc = ((crc >> 8) | (crc << 8)) & 0xFFFF
            crc = crc ^ i
            crc = (((crc & 0xFF) & 0xFFFF) >> 4) ^ crc
            crc = (crc ^ ((crc << 8) << 4) & 0xFFFF)
            crc = crc ^ (((crc & 0xFF) << 4) << 1 & 0xFFFF)
        return '{:0>4x}'.format(crc)

    @classmethod
    def str_to_hex(cls,data):
        '''将data转为utf-8编码,16进制字符串'''
        data_hex = data.encode('utf-8').hex()
        return " ".join(re.findall(r".{2}", data_hex))


    @classmethod
    def ten_to_hex(cls, num, several=0):
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

    @classmethod
    def event_cmd(cls, event_time, event_NO, event_head, event_body):
        '''
        event_time: 年/月/日/时/分
        event_NO: 事项提醒编号
        event_head: 事项提醒头部
        event_body: 事项提醒备注内容
        '''
        years, months, days, hour, minute,= event_time.split('/')
        years = '{:0>4x}'.format(int(years))[2:]+'{:0>4x}'.format(int(years))[:2]
        months = '{:0>2x}'.format(int(months))
        days = '{:0>2x}'.format(int(days))
        hour = '{:0>2x}'.format(int(hour))
        minute = '{:0>2x}'.format(int(minute))
        event_time_hex = years + months + days + hour + minute
        event_NO_hex = '{:0>2x}'.format(int(event_NO))
        event_head_hex = event_head.encode('utf-8').hex()
        event_body_hex = event_body.encode('utf-8').hex()
        head_len = len(event_head_hex)
        body_len = len(event_body_hex)
        if head_len < 0x4a*2:
            event_head_hex = event_head_hex+'0'*(0x4a*2-head_len)
        if body_len < 0x95*2:
            event_body_hex = event_body_hex+'0'*(0x95*2-body_len)
        head_len_hex = '{:0>2x}'.format(head_len//2)
        body_len_hex = '{:0>2x}'.format(body_len//2)

        cmd = '33daaddaad01ff0036007c0000' + '01' + '01' + event_NO_hex + '000000' + event_time_hex + '00000102' + \
              head_len_hex + body_len_hex + event_head_hex + '00' + event_body_hex
        m = [int(m, 16) for m in re.findall(r".{2}", cmd)]
        c = cls.cal_crc(m)
        cmd = cmd + c[2:] + c[0:2]
        mtu = readYaml(filePath.wristPara)['mtu']*2
        cmd_list = [cmd[i:i + mtu] for i in range(0, len(cmd), mtu)]
        appcmd_list = []
        for i in range(len(cmd_list)):
            if i == 0:
                appcmd_list.append("-".join(re.findall(r".{2}", cmd_list[i])))
            else:
                appcmd_list.append('33-' + '-'.join(re.findall(r".{2}", cmd_list[i])))

        cmd_del = '33daaddaad01ff0036007c0000' + '02' + '01' + event_NO_hex + '000000' + event_time_hex + '00000101' + \
                              head_len_hex + body_len_hex + event_head_hex + '00' + event_body_hex
        m = [int(m, 16) for m in re.findall(r".{2}", cmd_del)]
        c = cls.cal_crc(m)
        cmd_del = cmd_del + c[2:] + c[0:2]
        mtu = readYaml(filePath.wristPara)['mtu']*2
        cmd_list_del = [cmd_del[i:i + mtu] for i in range(0, len(cmd_del), mtu)]
        appcmd_list_del = []
        for i in range(len(cmd_list_del)):
            if i == 0:
                appcmd_list_del.append("-".join(re.findall(r".{2}", cmd_list_del[i])))
            else:
                appcmd_list_del.append('33-' + '-'.join(re.findall(r".{2}", cmd_list_del[i])))
        cls.event_list.append(appcmd_list_del)
        return appcmd_list

    @classmethod
    def event_idw03_cmd(cls, event_time, event_NO, event_head, repeat='01'):
        '''
        event_time: 年/月/日/时/分
        event_NO: 事项提醒编号
        event_head: 事项提醒头部
        event_body: 事项提醒备注内容
        '''
        years, months, days, hour, minute,= event_time.split('/')
        years = '{:0>4x}'.format(int(years))[2:]+'{:0>4x}'.format(int(years))[:2]
        months = '{:0>2x}'.format(int(months))
        days = '{:0>2x}'.format(int(days))
        hour = '{:0>2x}'.format(int(hour))
        minute = '{:0>2x}'.format(int(minute))
        event_time_hex = years + months + days + hour + minute
        event_NO_hex = '{:0>2x}'.format(int(event_NO))
        event_head_hex = event_head.encode('utf-8').hex()
        head_len = len(event_head_hex)
        if head_len < 0x96*2:
            event_head_hex = event_head_hex+'0'*(0x96*2-head_len)
        cmd = '33daaddaad01ff003600180000' + '01' + '01' + event_NO_hex + '000000' + event_time_hex + '00'+ repeat +'010204' + \
                '75' + '00'*75 + event_head_hex
        m = [int(m, 16) for m in re.findall(r".{2}", cmd)]
        c = cls.cal_crc(m)
        cmd = cmd + c[2:] + c[0:2]
        mtu = readYaml(filePath.wristPara)['mtu']*2
        cmd_list = [cmd[i:i + mtu] for i in range(0, len(cmd), mtu)]
        appcmd_list = []
        for i in range(len(cmd_list)):
            if i == 0:
                appcmd_list.append("-".join(re.findall(r".{2}", cmd_list[i])))
            else:
                appcmd_list.append('33-' + '-'.join(re.findall(r".{2}", cmd_list[i])))
        cls.event_list.append(appcmd_list)
        cmd_del = '33daaddaad01ff003600180000' + '02' + '01' + event_NO_hex + '000000' + event_time_hex + '00'+ repeat +'010204' + \
                '75' + '00'*75 + event_head_hex
        m = [int(m, 16) for m in re.findall(r".{2}", cmd_del)]
        c = cls.cal_crc(m)
        cmd_del = cmd_del + c[2:] + c[0:2]
        mtu = readYaml(filePath.wristPara)['mtu']*2
        cmd_list_del = [cmd_del[i:i + mtu] for i in range(0, len(cmd_del), mtu)]
        appcmd_list_del = []
        for i in range(len(cmd_list_del)):
            if i == 0:
                appcmd_list_del.append("-".join(re.findall(r".{2}", cmd_list_del[i])))
            else:
                appcmd_list_del.append('33-' + '-'.join(re.findall(r".{2}", cmd_list_del[i])))

        return appcmd_list




    @classmethod
    def event_cmd_del_all(cls):
        '''返回数组后清空event_list'''
        event_list = cls.event_list
        cls.event_list = []
        return event_list

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
    event_time = '2022/06/27/21/33'
    event_NO = '03'
    event_head = '一二三四五六七八九十'
    # event_body = '一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九'
    # print(eventCmd.event_idw03_cmd(event_time, event_NO, event_head)[0])
    # print(eventCmd.event_idw03_cmd(event_time, event_NO, event_head)[1])
    # print(eventCmd.event_cmd(event_time, 1, event_NO, event_head, event_body)[1])

    # print(eventCmd.event_cmd(event_time, 2, event_NO, event_head, event_body))

    print(eventCmd.set_time(event_time))
