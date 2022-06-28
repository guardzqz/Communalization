import re

from Logs.log import Loggings
from lib.getConfig import getConfig
from lib.yamlMethod import readYaml, writeYaml
LOG = Loggings()
def writeType(path, types):
    LOG.info('写资源类型到文件', path, types)
    data = readYaml(path)
    data[list(data.keys())[-1]].append(types)
    writeYaml(path, data)


def enableCase():
    allcase = re.split('[,，]', getConfig('enable', 'case'))
    cnn = re.split('[,，]', getConfig('unable', 'case'))
    scope = re.findall('\w+?~\w+', getConfig('enable', 'case'))
    if scope:
        for s in scope:
            si = re.findall('(\w+)~(\w+)', s)[0]
            sj = [i for i in range(int(float(si[0])), int(float(si[1])+1))]
            allcase[allcase.index(s)] = sj
    allcase = [int(float(i)) for i in resolveflat(allcase)]
    if cnn:
        try:
            cnn = [int(float(i)) for i in resolveflat(cnn)]
            for i in cnn:
                allcase.remove(i)
        except:
            pass
    return allcase

def resolveflat(datas):
    '''展开列表'''
    # LOG.info('展开列表', datas)
    temp = []
    for i in datas:
        if isinstance(i, (list)):
            temp.extend(resolveflat(i))
        else:
            temp.append(i)
    return temp

if __name__ == '__main__':
    enableCase()

