from Logs.log import Loggings
from ble.V3common import judgeType
from config.filePath import filePath
from lib.OtherMethod import resolveflat
from lib.yamlMethod import readYaml

LOG = Loggings()

def connectcmd(func):
    def outer(*args, **kwargs):
        cmd = func(*args, **kwargs)
        return '-'.join(cmd)
    return outer


def processOuterV2(*args):
    funcname = args[0]
    def outer(func):
        def inter(*args, **kwargs):
            alldata = func(*args, **kwargs)
            base = V2ProBase(funcname=funcname)
            res = resolveflat([base, alldata])
            LOG.info('最终协议', res)
            return res
        return inter
    return outer

def V2ProBase(funcname):
    LOG.info('处理v2协议头', funcname)
    funcData = readYaml(filePath.bleExplain)[funcname]
    base = [judgeType(funcData['cmd']), judgeType(funcData['key'])]
    return base