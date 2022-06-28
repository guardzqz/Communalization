from ruamel import yaml

from Logs.log import Loggings

LOG = Loggings()
def readYaml(file):
    '''读取yaml，返回数据类型为字典'''
    # LOG.info('读取yaml文件', file)
    with open(file, 'r', encoding='utf-8') as f:
        data = yaml.load(f.read(), Loader=yaml.RoundTripLoader)
    # LOG.info(data)
    return data


def writeYaml(yamlpath, data=None):
    LOG.info('写入yaml文件', yamlpath, data)
    with open(yamlpath, "w", encoding="utf-8") as f:
        if data is None:
            return
        yaml.dump(data, f, allow_unicode=True, Dumper=yaml.RoundTripDumper)


if __name__ == '__main__':
    dd = readYaml(r'D:\zqz\project\dec\config/caseTemp\alarm.yaml')
    print(dd)
    dd[6] = [111]
    writeYaml(r'D:\zqz\project\dec\config/caseTemp\alarm.yaml', dd)
    aa = readYaml(r'D:\zqz\project\dec\config/caseTemp\alarm.yaml')

    print(aa)