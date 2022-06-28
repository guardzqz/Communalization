import ruamel
import re
from lib.yamlMethod import writeYaml, readYaml
from method.OperationDir import clearStatus, delDir
from Event_class import Event







# 解决eval执行yaml时,报错问题
def ordereddict(para):
    return dict(para)

class test_Event(Event):
    def __init__(self):
        Event.__init__(self)
        self.case_data = readYaml('event_data.yaml')
        self.case_exe = readYaml('event_exe.yaml')
    # 解析测试数据,存为类变量.
    def parse_data(self, case_data):
        for key in case_data:
            if 'event_rem_' in key:
                exec('self.' + key + ' = case_data["' + key + '"]')    #self.event_rem_1 = case_data['event_rem_1']
            elif 'entry' == key:
                exec('self.'+ key + ' = case_data["' + key + '"]')
            elif 'head_bodys' in key:
                data = case_data[key]
                self.event_rem_list = [{'event_time':self.time_add(data['event_time'],'n',6*(i-data['start_count'])),
                                        'event_NO': str(i),
                                        'event_head':data['head']+str(i-data['start_count']+1),
                                        'event_body':data['body']+str(i-data['start_count']+1),}
                                       for i in range(data['start_count'],data['end_count'])]
                for i in range(data['start_count'], data['end_count']):
                    exec('self.event_rem_%s = self.event_rem_list[%s]' % (str(i), str(i-data['start_count'])))
            elif 'head_body' == key:
                data = case_data[key]
                self.event_rem_list = [{'event_time': '2023/01/03/09/00', 'event_NO': str(i + 1),'event_head': data[i][0],'event_body': data[i][1]} for i in range(len(data))]
                for i in range(len(self.event_rem_list)):
                    exec('self.event_rem_%s = self.event_rem_list[%s]' % (str(i + 1), str(i)))
            elif 'language' in key:
                exec('self.'+ key + ' = case_data["' + key + '"]')
                entry_0 = [event_rem['event_head'] +', '+ event_rem['event_body'] for event_rem in self.event_rem_list]
                self.entry = []
                for e in entry_0:
                    for _ in range(4):
                        self.entry.append(e)

    def while_operation(self, para_list):
        for i in range(1,para_list[0]+1):
            for operation in para_list[1:]:
                if type(operation) in (ruamel.yaml.comments.CommentedMap,dict):
                    k, v = self.get_key_value(operation)
                    v = re.sub('_i', '_%d'%i, str(v))
                    try:
                        eval('self.' + k + '(' + str(v) + ')')   #当 yaml v值为列表时执行
                    except:
                        eval('self.' + k + '(self.' + str(v) + ')')       #当 yaml v值为字符串时执行
                    continue
                self.execute_operation(operation)

    def execute_operation(self, operation):
        if operation == 'p':
            self.sleep_camera(self.yamlpath, self.entry.pop(0))  #获取并删除当前拍照词条
            print('test: ',self.entry.pop(0))
            pass
        elif type(operation) == str:
            eval('self.' + operation + '()')
        elif type(operation) in (ruamel.yaml.comments.CommentedMap,dict):
            k, v = self.get_key_value(operation)
            try:
                eval('self.' + k + '(' + str(v) + ')')  # 当 yaml v值为列表时执行
            except:
                eval('self.' + k + '(self.' + str(v) + ')')  # 当 yaml v值为字符串时执行
        else:
            print('operation参数错误')

    def test_case(self, case_NO):
        case_data = self.case_data['case_data_' + str(case_NO)]
        self.parse_data(case_data)
        print('解析测试数据完成')
        case_exe = self.case_exe['case'+str(case_NO)]
        for exe in case_exe:
            self.execute_operation(exe)

    def run_case(self):
        self.demotext("74-0b-01")
        self.demotext("74-07-ff-ff")
        self.re_page()
        print('开始执行测试用例')
        case_txt_list = ['弹出删除icon时，操作检查', '标题，内容上限，时间格式检查', '事项提醒界面的提醒时间及切换时间制检查', '事项详情页时间及时间制切换检查', '提醒事项排序检查', '提醒事项数量上限检查','test']
        writeYaml(self.yamlpath, self.data)
        for case_NO in range(4,8):
            pic = self.picfield()
            clearStatus()
            self.data = readYaml(self.yamlpath) if readYaml(self.yamlpath) else {}
            self.data[case_txt_list[case_NO-1]] = []
            writeYaml(self.yamlpath, self.data)
            #执行用例
            self.test_case(case_NO)
            self.writeExcel(pic, case_txt_list[case_NO-1])  # 写入excel

if __name__ == '__main__':
    test = test_Event()
    test.run_case()