#coding=utf-8
from dataclasses import dataclass


@dataclass
class icon_location:
    '''
    手环所有功能
    基础icon命名及位置
    位置参数都传元组，元组内参数支持int及float
    例如：健康数据:tuple=（1,2）
    '''
    健康数据: tuple = (0, 0)
    倒计时: tuple = (0, 0)
    秒表: tuple = (0, 0)
    呼吸训练: tuple = (0, 0)
    闹钟: tuple = (0, 0)
    音乐: tuple = (0, 0)
    女性健康: tuple = (0, 0)
    寻找手机: tuple = (0, 0)
    天气: tuple = (0, 0)
    心率: tuple = (0, 0)
    体温: tuple = (0, 0)
    睡眠: tuple = (0, 0)
    压力: tuple = (0, 0)
    血氧: tuple = (0, 0)
    噪音: tuple = (0, 0)
    手电筒: tuple = (0, 0)










if __name__ == '__main__':
    a = icon_location(倒计时=(7,9),健康数据=5)
    # print(a.倒计时)
    # print(a.健康数据)
    # print(a.__dict__)
    # b= enter_icon()
    # print(b.倒计时)
    # b=icon_action()
    # b.inter_icon("倒计时")
    # b.find_icon("闹钟")

