#coding=utf-8
import os
import sys
def app_path():
    """Returns the base application path."""
    if hasattr(sys, 'frozen'):
        # Handles PyInstaller
        return os.path.dirname(os.path.dirname(sys.executable))
    return os.path.dirname(os.path.dirname(__file__))

PATHONE = lambda p: os.path.join(app_path(), p)


class filePath:
    '''
    路径配置文件
    '''
    BASE_PATH = os.path.split(os.path.dirname(__file__))[0]

    bleExplain = PATHONE(r'config/blee/bleExplain.yaml')  # 手环蓝牙协议方法解释
    wristPara = PATHONE(r'config/blee/wrist.yaml') # 手环参数
    ICON_EVENT_ACTION = PATHONE("config\icon_event_action.yaml")  # demo 路径
    CONFIG_FILE = PATHONE("config\config.ini")  # 配置文件的path
    USERSARGS = PATHONE(r"config\user\users.yaml")  # 用户配置
    eventPara =  PATHONE(r"config\case_data\event_data.yaml")
    event_exe = PATHONE(r"config\case_data\gt02_event_exe.yaml")
    menstPara = PATHONE(r'config\case_data\menst_data.yaml')  # 女性健康参数
    watch_cmd = PATHONE(r'config\watch_cmd.yaml')  # 手表指令
    var_list = PATHONE(r'testCase\var_list.yaml')  # 手表指令


    DB_FILE = PATHONE("config\caseDb")  # 存放用例数据库
    CASE_FILE = PATHONE("config\wrist")  # 存放用例excel
    CASETEMP_DIR = PATHONE(r'config/caseTemp')  # 存放模块的图片生成序列
    RESULTSTATIC = PATHONE(r'config\resultStatic') # 结果HTML文件的样式

    DESCRIPTION = PATHONE(r'TEXT/拍照序列.txt')  # 拍照录像说明

    OSOURCES_DIR = PATHONE(r'photo\originSources')
    FSOURCES_DIR = PATHONE(r'photo\finishFigure')
    OPICTURES_DIR = PATHONE(r'photo\originSources\pictures')
    FPICTURES_DIR = PATHONE(r'photo\finishFigure\pictures')
    OVIDEOS_DIR = PATHONE(r'photo\originSources\videos')
    FVIDEOS_DIR = PATHONE(r'photo\finishFigure\videos')

    ZIPSTORAGE_DIR = PATHONE(r'zipStorage') # 原图片视频备份
    RESULTDIR = PATHONE(r'result')  # 结果文件夹



    LOG_DIR = PATHONE(r'Logs')  # 日志


    music_cmd = PATHONE(r'testCase\MUSIC\music_cmd.yaml')  # 音乐指令
    all_cmd = PATHONE(r'testCase\all_data.yaml')  # 指令集
