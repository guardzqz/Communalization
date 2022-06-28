import re
import time

from Logs.log import Loggings
from config.filePath import filePath

import sys

from lib.base_action import icon_location
from lib.transcodingCmd import transcoding_screen
from lib.yamlMethod import readYaml
from method.findBle import findBle

LOG = Loggings()
class Operation_wrist:
    '''
    手环的操作方法
    '''


    def 上滑(self,x=0,y=0):
        """
        "上滑":6,
        :return:
        """
        return transcoding_screen(6, x, y)



    def 下滑(self, x=0, y=0):
        return transcoding_screen(7, x, y)



    def 左滑(self, x=0, y=0):
        return transcoding_screen(8, x, y)


    def 右滑(self, x=0, y=0):
        return transcoding_screen(9, x, y)


    def 点击(self, x=0, y=0):
        return transcoding_screen(1, x, y)


    def 长按(self, x=0, y=0):
        '''
        长按位置相对固定
        :param x:
        :param y:
        :return:
        '''
        return transcoding_screen(13, x, y)


    def 短按右键(self):
        return "7401000200020004"


    def 长按右键(self):
        return "7401000200020003"


    def 进入自动化指令(self):
        return "740b01"


    def 退出自动化指令(self):
        return "740b02"


    def 长亮屏(self):
        return "7407ffff"

    def 重启(self):
        return 'f001'

    def app发起运动(self):
        return '10010000000030000000000001'

    def 灭屏(self):
        return "74070000"

    def 等待(self,sec):
        time.sleep(float(sec))

class icon_action(icon_location,Operation_wrist):
    '''
    依据传参进入icon
    '''
    def __init__(self, bluemethod):
        self.ble_method=bluemethod
    def inter_icon(self,name):
        '''
        :param name: 进入手表一级界面方法
        :return:
        '''
        global icon_name
        # a=0
        exec(f"global icon_name;icon_name=self.{name}")
        x,y = icon_name
        inter_icon_cmd = transcoding_screen(1, x, y)
        print(inter_icon_cmd)
        self.ble_method.sendData(inter_icon_cmd)


    def find_icon(self,name):
        '''
        name 为模块名称
        :return:
        '''
        global action_cmd
        icon_path = readYaml(filePath.ICON_EVENT_ACTION)[name]["路径"]
        wrist_method_nochange = readYaml(filePath.ICON_EVENT_ACTION)["手环方法"]["不可变"]
        # for action in icon_path:
        try:

            for i in icon_path:
                x_y = re.findall(r'\d+(?:\.\d+)?', i)
                action = re.findall(r'[\u4e00-\u9fa5]+', i)
                if len(action) > 1:
                    if "-" in i:
                        self.judge_action_location(name, i)
                    continue
                if self.judge_action(action[0], name):
                    self.base_action(name, action)
                    continue
                if not self.judge_action(action[0], name):
                    if len(x_y):
                        self.With_parameters_method(action[0], x_y)
                    else:
                        self.With_parameters_method(action[0])
                    continue
                if action[0] in wrist_method_nochange:
                    self.With_parameters_method(action[0])
                    continue
        except Exception as e:
            print(e)
            raise ValueError(f"执行{sys._getframe(0).f_code.co_name}函数{action}参数错误！")



    def public_wristmethod(self,name="可变"):
        '''
        获取手环方法
        :return:
        '''
        methods =readYaml(filePath.ICON_EVENT_ACTION)["手环方法"][name]
        return methods




    def judge_action(self,action,name=None):
        '''
        判定元素在操作方法里还是在配置 操作层中,还是方法中
        :return:
        '''
        operational = readYaml(filePath.ICON_EVENT_ACTION)[name]
        action_list = list(dict(operational).keys())

        if action in action_list:
            return True
        elif action in self.public_wristmethod():
            return False




    def base_action(self,name,basename,wristaction="点击"):
        '''
        name 为icon名称

        def spam(a, b, c, d):
            print(a, b, c, d)
        from functools import partial
            # >>> s1 = partial(spam, 1) # a = 1
        调用基础操作层方法
        name 为icon的名称
        basename 为icon操作层的命名
        wristaction 为operationwrist 需要传参的操作事件
        :return:
        '''
        global action_cmd
        action_name = readYaml(filePath.ICON_EVENT_ACTION)[name][basename]
        x, y = action_name
        exec(f"global action_cmd; action_cmd=self.{wristaction}({x},{y})")

        self.ble_method.sendData(action_cmd)



    def With_parameters_method(self,action,x_y=None):
        '''
        处理带参数及不带参数方法
        :return:
        '''
        global action_cmd
        #c
        if x_y:
            if  len(x_y) == 2:
                x, y = [float(i) for i in x_y]
                exec(f"global action_cmd; action_cmd=self.{action}({x},{y})")
            #处理时间
            elif len(x_y)== 1:
                exec(f"global action_cmd; action_cmd=self.{action}({float(x_y[0])})")
        else:
            exec(f"global action_cmd; action_cmd=self.{action}()")
        self.ble_method.sendData(action_cmd)


    def judge_action_location(self,name,action_event):
        '''
        获取手环操作的位置
        :return:
        '''
        action_list = re.findall(r'[\u4e00-\u9fa5_a-zA-Z]+', action_event)
        action_name = readYaml(filePath.ICON_EVENT_ACTION)["手环方法"]["可变"]
        if action_list[0] in action_name:
            self.base_action(name, action_list[1], action_list[0])
        else:
            self.base_action(name, action_list[0], action_list[1])


    def event_action(self,name,event):
        '''
        自定义事件方法
        name 为模块名称，event 为自定义事件下的名称
        :return:
        '''
        global action_cmd
        icon_path = readYaml(filePath.ICON_EVENT_ACTION)[name]["自定义事件"][event]
        event_key = list(dict(readYaml(filePath.ICON_EVENT_ACTION)[name]["自定义事件"]).keys())
        event_key.remove(event)
        wrist_method_nochange = readYaml(filePath.ICON_EVENT_ACTION)["手环方法"]["不可变"]
        for i in icon_path:
            if i in event_key:

                self.event_action(name, i)
                continue
            x_y = re.findall(r'\d+(?:\.\d+)?', i)
            action = re.findall(r'[\u4e00-\u9fa5_a-zA-Z]+', i)
            if len(action)>1:
                if "-" in i:
                    self.judge_action_location(name, i)
                continue
            if self.judge_action(action[0], name):
                self.base_action(name, action)
                continue
            if not self.judge_action(action[0], name):
                if len(x_y):
                    self.With_parameters_method(action[0], x_y)
                else:
                    self.With_parameters_method(action[0])
                continue
            if action[0] in wrist_method_nochange:
                self.With_parameters_method(action[0])
                continue















if __name__ == '__main__':
    x=icon_action(findBle())

    # x.event_action("闹钟", '返回首页')
    # x.judge_action_location("闹钟","删除闹钟-长按")
    # print(x.With_parameters_method('长按右键'))
    # time.sleep(3)
    # # for i in range(5):
    # # print(x.With_parameters_method('右滑', (320, 180)))
    # print(x.With_parameters_method('点击', (170, 310)))
    # x.find_icon("秒表")
    # self.wrist_action.find_icon("秒表")

    x.event_action('闹钟', '返回首页')
    # x.test()
    # print(x.With_parameters_method('长按右键'))
    # print(x.judge_action('上滑', "闹钟"))
    # print(x.public_wristmethod())
    # x.inter_icon("闹钟")
#