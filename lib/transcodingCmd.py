
import re


def transcoding_screen(num_cmd, x, y):
    '''
    传入x轴或y轴坐标，转成16进制形式
    :param num_cmd:为操作码
    :param cell:
    :return:
    :action_code:操作类型代码
    74-01-xx--xx-yy-yy-00-01
    '''

    args = float(x), float(y)
    x_y = "7401"  # 头信息
    code = "".join(["{:0>4x}".format(round(i+2)) for i in args])#i+2 是为了将坐标点至于控件上
    code=x_y + code+"{:0>4}".format(num_cmd)
    return code


def transcoding(num, cmd, several=8):
    '''
    根据单元格指令和数值转换成指令
    :param num: 需转化的值
    :param cell:
    :return:
    '''
    num=float(num)
    trans_code = ten_to_hex(num, several)  # 生成几位
    trans_code = "".join([cmd, trans_code])
    return trans_code



def ten_to_hex(num, several=0):
    """
    num为待转换为16进制数据，
    text为excel单元格中读取到的命令
    serveral 为uint32_t value
    """
    num = round(float(num))
    several =2 if several==0 else several
    trans_code = '{:0>{several}x}'.format(int(num), several=several) # 小端序  several设置位数
    trans_code="".join(re.findall(".{2}",trans_code)[::-1])
    return trans_code




if __name__ == '__main__':
    # print(transcoding_screen(5,20,160))
    print(transcoding_screen(6,140,170))