import ruamel
import re
from lib.yamlMethod import writeYaml, readYaml
from method.OperationDir import clearStatus, delDir
from sport_record_class import SportExcel


'''
    说明：
        1. 编码：longt
        2. 开始时间：2022-6-13
        3. 最近更新：2020-6-13
        4. 简介:执行运动记录模块
'''


# 解决eval执行yaml时,报错问题
def ordereddict(para):
    return dict(para)


class Test(SportExcel):

    def __init__(self):

        SportExcel.__init__(self)

        self.case_data = readYaml('sport_record_data.yaml')

        self.case_exe = readYaml('sport_record_caselist.yaml')


    # 解析测试数据,存为类变量.
    def judgment(self,case_data):

        for key in case_data:

            if 'illustrate' == key:

                exec('self.' + key + ' = case_data["' + key + '"]')
                self.illustrate = case_data[key]


            elif 'to_data_' in  key:

                exec('self.' + key + ' = case_data["' + key + '"]')



    #行为函数
    def execute(self, execute):

        if execute == 'p':
            a = self.illustrate.pop(0)
            print(self.yamlpath, a)
            self.sleep_camera(self.yamlpath, str(a))

        elif type(execute) == str:
            eval('self.' + execute + '()')

        elif type(execute) in (ruamel.yaml.comments.CommentedMap,dict):
            k, v = self.get_key_value(execute)
            try:
                eval('self.' + k + '(' + str(v) + ')')    # 当 yaml v值为列表时执行
            except:
                eval('self.' + k + '(self.' + str(v) + ')')


    #循环执行
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
                self.execute(operation)


    def test_case(self, case_NO):
        case_data = self.case_data['test_data_' + str(case_NO)]
        self.judgment(case_data)
        print('解析测试数据完成')
        case_exe = self.case_exe['case_list_'+str(case_NO)]
        for exe in case_exe:
            self.execute(exe)

    def run_case(self):

        print('开始执行测试用例')
        case_txt_list = ['无运动记录','时间目标','卡路里目标','距离目标','户外跑步','徒步','走路','户外骑行','室内骑行','划船机','椭圆机','瑜伽','运动记录列表']
        writeYaml(self.yamlpath, self.data)
        for case_NO in range(13,14):
            pic = self.picfield()
            clearStatus()
            self.data = readYaml(self.yamlpath) if readYaml(self.yamlpath) else {}
            self.data[case_txt_list[case_NO-1]] = []
            writeYaml(self.yamlpath, self.data)
            #执行用例
            self.demotext("74-0b-01")
            self.demotext("74-07-ff-ff")
            self.test_case(case_NO)
            self.demotext("74-0b-02")
            self.writeExcel(pic, case_txt_list[case_NO-1]) # 写入excel
            print('测试用例%s执行完成'%case_txt_list[case_NO-1])



if __name__ == '__main__':

    test = Test()
    test.run_case()
