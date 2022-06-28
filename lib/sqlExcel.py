
from pandas import read_excel, concat, read_sql
import os
from sqlalchemy import create_engine, BigInteger, Text

from Logs.log import Loggings
from config.filePath import filePath

from lib.getConfig import getConfig

LOG = Loggings()
class sqlExcel:
    '''
    将用例输出到sql，db和table名在config.ini配置
    '''
    def __init__(self, col='用例编号', sheett=None, headerr=0):
        '''
        初始化配置，在创建db和读取db的时候都要用到
        :param col: 筛选不重复的列
        :param sheett: 要读取的子表，默认所有，传参格式为列表 [1,2,'表1']
        :param headerr: 将第几行设为表头，默认第一行，传参格式为整数
        '''
        LOG.info('数据库操作...')
        self.sheett = sheett
        self.headerr = headerr
        self.col = col
        self.module = getConfig('module', 'project')
        # 数据库引擎，没有则创建
        self.engine = create_engine('sqlite:///'+filePath.DB_FILE+os.sep+getConfig('wrist', 'project')+'.db', echo=True)

    def existFile(self, path):
        '''
        excel文件是否存在
        '''
        LOG.info('判断文件是否存在', path)
        if os.path.exists(path):
            if os.path.splitext(path)[1] in ['.xls', '.xlsx']:
                return True
        else:
            raise Exception('文件不存在', path)

    def readExcel(self, path):
        '''
        读取excel文件，默认读所有表，去掉col列为nan的情况，如果指定col列有重复，不再继续
        :param path:
        :return:
        '''
        LOG.info('读取excel文件', path)
        if self.existFile(path):
            data = read_excel(io=path, sheet_name=self.sheett, header=self.headerr)
            if not isinstance(data, dict):
                data = [data]
            data = concat(data)
            if True in data.duplicated(subset=[self.col]).values:
                raise Exception("数据有重复")
            data = data.dropna(subset=[self.col])
            return data

    def dataToSql(self):
        '''
        根据用例excel，创建table，导入数据
        :return:
        '''
        LOG.info('将数据转到数据库')
        for i in os.listdir(filePath.CASE_FILE+os.sep+getConfig('wrist', 'project')):
            if self.module == os.path.splitext(i)[0]:
                data = self.readExcel(filePath.CASE_FILE+os.sep+getConfig('wrist', 'project')+os.sep+i)
                data.fillna(method="ffill",inplace=True)#空值数据往下填充nan数据
                dtypedict = {
                    '用例编号':BigInteger,
                    '模块':Text,
                    '前置条件':Text,
                    '操作步骤':Text,
                    '预期结果':Text,
                    '结果':Text
                }
                data.to_sql(self.module, con=self.engine, if_exists='replace', index=False, dtype=dtypedict)
                break

    def readData(self, cols):
        '''
        读取数据库数据，根据sql查询，以cols列查询
        :return: 返回一行数据
        '''
        LOG.info('读取数据列', cols)
        sqll = f'select * from {self.module} where 用例编号={cols}'
        frame = read_sql(sqll, self.engine)
        return frame.loc[0].to_dict()

if __name__ == '__main__':
    sqlExcel().dataToSql()
    # sqlExcel().readData(12)