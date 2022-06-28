#encoding=utf-8
import time
from shutil import copy

import cv2
from bottle import template
import webbrowser
import os

from Logs.log import Loggings
from config.filePath import filePath
from lib.getConfig import getConfig

from lib.sqlExcel import sqlExcel
from lib.yamlMethod import readYaml
from method.OperationDir import getPicYield, getDescriptionYeild

LOG = Loggings()
t = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
class resultH5:
    @classmethod
    def H5(cls, module):
        LOG.info('生成结果', module)
        destPath = os.path.join(filePath.RESULTDIR, f"{module}", t)
        os.makedirs(destPath)
        h5path = os.path.join(destPath, f"{module+'-'+t}" + ".html")
        casedata = resultH5.getData(module, destPath+os.sep)
        htmls = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{{ title }}</title>
        <link rel="stylesheet" href="result.css" type="text/css">
        <script type="text/javascript" src="FileSaver.js"></script>
        <script type="text/javascript" src="result.js"></script>
    </head>
    <body>
    <h1>用例结果</h1>
    <div class="contain-all">
    '''
        htmle = '''
        </div>
        <button type="button" onclick="resultBtn()">获取最终结果</button>
        </body>
    </html>
        '''
        template_demo = '''
            <div class="contain-row">
            <div class="case-index roww" onclick="sty({{ index }})">
                <p>{{ index }}</p>
                <p>
                    <input type="radio" name={{ index }} value="notYet" id="notYet{{ index }}" checked><label for="notYet{{ index }}">未操作</label>
                    <input type="radio" name={{ index }} id="yes{{ index }}" value="yes"><label for="yes{{ index }}">通过</label>
                    <input type="radio" name={{ index }} id="no{{ index }}" value="no"><label for="no{{ index }}">未通过</label>
                </p>
            </div>
            <div class="case-title">
                % for pd in case:
                    <p>{{ pd }}</p>
                %end
            </div>
            <div class="case-text">
                % for pd in case:
                    <p>{{ case[pd] }}</p>
                %end
            </div>
            <div class="imgarea">
                % for pic, px, explain in pic:
                    <div>
                        % if pic[-3:]=='jpg' or pic[-3:]=='png':
                        <img src="{{ pic }}" height="{{ px[1] }}">
                        % elif pic[-3:]=='mp4' or pic[-3:]=='avi':
                        <video width="{{ px[0] }}" height="{{ px[1] }}" controls autoplay>
                            <source src="{{ pic }}" type="video/mp4">
                        </video>
                        %end
                        <p>{{ explain }}</p>
                    </div>
                % end
            </div>
            <div class="atextarea">
                    <textarea>备注</textarea>
                </div>
        </div>
        '''
        if casedata:
            htmls = template(htmls, title=module+t+'.html')
            with open(h5path,'wb') as f:
                f.write(htmls.encode('utf-8'))
            index = 1
            for case, pic in casedata:
                html = template(template_demo, case=case, pic=pic, index=index)
                with open(h5path, 'ab+') as f:
                    f.write(html.encode('utf-8'))
                index+=1
            with open(h5path, 'ab+') as f:
                f.write(htmle.encode('utf-8'))
            resultH5.copyStaticFile(filePath.RESULTSTATIC, destPath, ['FileSaver.js', 'result.js', 'result.css'])
            #使用浏览器打开html
            webbrowser.open(h5path)

    @classmethod
    def getData(cls, module, destPath):
        '''
        获取资源数据
        :param module: 模块
        :param destPath: 生成结果的文件地址
        :return:
        '''
        LOG.info('获取结果需要的资源', module, destPath)
        camera_pic = getPicYield(destPath+'pictures', filePath.FPICTURES_DIR)
        screen_pic = getPicYield(destPath+'videos', filePath.FVIDEOS_DIR)
        descript_pic = getDescriptionYeild(filePath.DESCRIPTION)
        alldata = []
        yamlpath = filePath.CASETEMP_DIR+os.sep+module+'.yaml'
        LOG.info('yamlpath', yamlpath)
        if os.path.exists(yamlpath):
            data = readYaml(yamlpath)
            if data:
                for case, sources in data.items():
                    case = sqlExcel().readData(case)
                    sources = cls.getSource(sources, camera_pic, screen_pic, descript_pic)
                    LOG.info('生成数据', alldata)
                    alldata.append([case, sources])
            return alldata


    @classmethod
    def getSource(cls, sources, camera_pic, screen_pic, descript_pic):
        LOG.info('当前需要资源', sources)
        piclist = []
        for s in sources:
            px = (1000, 1000)
            pic, newpic = None, None
            try:
                if s in ['p']:
                    pic = camera_pic.__next__()
                    px = cv2.imread(pic).shape[:2]
                    newpic = os.path.join('pictures', os.path.basename(pic))
                    LOG.info('piccamera', pic, newpic)
                elif s in ['s']:
                    pic = screen_pic.__next__()
                    newpic = os.path.join('videos', os.path.basename(pic))
                    LOG.info('picscreen', pic)
            except Exception as e:
                LOG.exception('找不到资源', e)
            finally:
                if s in ['p','s'] and pic and newpic:
                    try:
                        descript = descript_pic.__next__()
                    except Exception as e:
                        print('找不到说明', e)
                        descript = ''
                    maxpixel = int(getConfig('maxpixel', 'photo'))
                    if px[1]>maxpixel:
                        px = (maxpixel, maxpixel)
                    piclist.append([newpic, px, descript])
                    LOG.info('piclist', piclist)
                else:
                    piclist.append(['', px, '缺资源'])
        return piclist

    @classmethod
    def copyStaticFile(cls, source, target, filelist):
        '''
        拷贝文件到新地址
        :param source: 原文件夹
        :param target: 目标文件夹
        :param flielist: 文件名
        :return:
        '''
        LOG.info('拷贝文件夹', source,'文件', filelist, '到', target)
        for i in filelist:
            copy(source+os.sep+i, target)


if __name__ == '__main__':
    resultH5.H5('sport')