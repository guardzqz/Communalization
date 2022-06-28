from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QRegExp, QDateTime
from PyQt5.QtGui import QRegExpValidator, QIntValidator
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QLineEdit, QPushButton, QSplitter, QGridLayout, QTextEdit, \
    QComboBox, QDateTimeEdit, QFormLayout, QDateEdit, QTimeEdit


class MenstrualUI():
    def setupUi(self, plate):
        plate.setObjectName('plate')
        InterRegExp = QRegExp("[0-9]{0,2}")
        pIntValidator = QRegExpValidator()
        pIntValidator.setRegExp(InterRegExp)

        LongInterRegExp = QRegExp("[0-9]*")
        LongInterValidator = QRegExpValidator()
        LongInterValidator.setRegExp(LongInterRegExp)

        self.cmdlayout = QGridLayout()

        self.setDateTimeEdit = QDateTimeEdit()
        self.setDateTimeEdit.setObjectName('setDateTimeEdit')
        # self.setDateTimeEdit.setCalendarPopup(True)
        self.setDateTimeEdit.setDateTime(QDateTime.currentDateTime())

        self.timeZoneEdit = QLineEdit()
        self.timeZoneEdit.setObjectName('timeZoneEdit')
        self.timeZoneEdit.setPlaceholderText('时区')
        self.timeZoneEdit.setText('8')

        self.setTimebtn = QPushButton()
        self.setTimebtn.setObjectName('setTimebtn')

        self.onoffcb = QComboBox()
        self.onoffcb.setObjectName('onoffcb')



        self.menstruallenEdit = QLineEdit()
        self.menstruallenEdit.setObjectName('menstruallenEdit')
        self.menstruallenEdit.setValidator(pIntValidator)
        self.menstruallenEdit.setPlaceholderText('经期长度')

        self.menstrualcycleEdit = QLineEdit()
        self.menstrualcycleEdit.setObjectName('menstrualcycleEdit')
        self.menstrualcycleEdit.setValidator(pIntValidator)
        self.menstrualcycleEdit.setPlaceholderText('经期周期')


        self.lastMenstrualEdit = QDateEdit()
        self.lastMenstrualEdit.setObjectName('lastMenstrualEdit')
        self.lastMenstrualEdit.setDateTime(QDateTime.currentDateTime())

        self.IntervalEdit = QLineEdit()
        self.IntervalEdit.setObjectName('IntervalEdit')
        self.IntervalEdit.setValidator(pIntValidator)
        self.IntervalEdit.setPlaceholderText('经期跟排卵日间隔')

        self.beforeEdit = QLineEdit()
        self.beforeEdit.setObjectName('beforeEdit')
        self.beforeEdit.setValidator(pIntValidator)
        self.beforeEdit.setPlaceholderText('排卵期前易孕天数')

        self.afterEdit = QLineEdit()
        self.afterEdit.setObjectName('afterEdit')
        self.afterEdit.setValidator(pIntValidator)
        self.afterEdit.setPlaceholderText('排卵期后易孕天数')

        self.notifyflagcb = QComboBox()
        self.notifyflagcb.setObjectName('notifyflagcb')

        self.setMenstrualV2btn = QPushButton()
        self.setMenstrualV2btn.setObjectName('setMenstrualV2btn')

        self.startdayEdit = QLineEdit()
        self.startdayEdit.setObjectName('startdayEdit')
        self.startdayEdit.setValidator(pIntValidator)
        self.startdayEdit.setPlaceholderText('经期开始提前提醒')

        self.ovulationdayEdit = QLineEdit()
        self.ovulationdayEdit.setObjectName('ovulationdayEdit')
        self.ovulationdayEdit.setValidator(pIntValidator)
        self.ovulationdayEdit.setPlaceholderText('排卵期提前提醒')

        self.hourEdit = QTimeEdit()
        self.hourEdit.setObjectName('hourEdit')
        self.hourEdit.setTime(QDateTime.currentDateTime().time())


        self.pergnancyBeforeEdit = QLineEdit()
        self.pergnancyBeforeEdit.setObjectName('pergnancyBeforeEdit')
        self.pergnancyBeforeEdit.setValidator(pIntValidator)
        self.pergnancyBeforeEdit.setPlaceholderText('易孕期开始提前天数')


        self.pergnancyAfterEdit = QLineEdit()
        self.pergnancyAfterEdit.setObjectName('pergnancyAfterEdit')
        self.pergnancyAfterEdit.setValidator(pIntValidator)
        self.pergnancyAfterEdit.setPlaceholderText('易孕期结束提前天数')

        self.menstrualendEdit = QLineEdit()
        self.menstrualendEdit.setObjectName('menstrualendEdit')
        self.menstrualendEdit.setValidator(pIntValidator)
        self.menstrualendEdit.setPlaceholderText('经期结束提前天数')

        self.setMenstrualRemindV2btn = QPushButton()
        self.setMenstrualRemindV2btn.setObjectName('setMenstrualRemindV2btn')

        self.menstrualstartEdit1 = QDateEdit()
        self.menstrualstartEdit1.setObjectName('menstrualstartEdit1')
        self.menstrualstartEdit1.setDateTime(QDateTime.currentDateTime())

        self.menstrualdayEdit1 = QLineEdit()
        self.menstrualdayEdit1.setObjectName('menstrualdayEdit1')
        self.menstrualdayEdit1.setValidator(pIntValidator)
        self.menstrualdayEdit1.setPlaceholderText('经期长度')

        self.cycledayEdit1 = QLineEdit()
        self.cycledayEdit1.setObjectName('cycledayEdit1')
        self.cycledayEdit1.setValidator(pIntValidator)
        self.cycledayEdit1.setPlaceholderText('周期长度')

        self.menstrualstartEdit2 = QDateEdit()
        self.menstrualstartEdit2.setObjectName('menstrualstartEdit2')
        self.menstrualstartEdit2.setDateTime(QDateTime.currentDateTime())

        self.menstrualdayEdit2 = QLineEdit()
        self.menstrualdayEdit2.setObjectName('menstrualdayEdit2')
        self.menstrualdayEdit2.setValidator(pIntValidator)

        self.cycledayEdit2 = QLineEdit()
        self.cycledayEdit2.setObjectName('cycledayEdit2')
        self.cycledayEdit2.setValidator(pIntValidator)

        self.menstrualstartEdit3 = QDateEdit()
        self.menstrualstartEdit3.setObjectName('menstrualstartEdit3')
        self.menstrualstartEdit3.setDateTime(QDateTime.currentDateTime())

        self.menstrualdayEdit3 = QLineEdit()
        self.menstrualdayEdit3.setObjectName('menstrualdayEdit3')
        self.menstrualdayEdit3.setValidator(pIntValidator)

        self.cycledayEdit3 = QLineEdit()
        self.cycledayEdit3.setObjectName('cycledayEdit3')
        self.cycledayEdit3.setValidator(pIntValidator)

        self.menstrualstartEdit4 = QDateEdit()
        self.menstrualstartEdit4.setObjectName('menstrualstartEdit4')
        self.menstrualstartEdit4.setDateTime(QDateTime.currentDateTime())

        self.menstrualdayEdit4 = QLineEdit()
        self.menstrualdayEdit4.setObjectName('menstrualdayEdit4')
        self.menstrualdayEdit4.setValidator(pIntValidator)

        self.cycledayEdit4 = QLineEdit()
        self.cycledayEdit4.setObjectName('cycledayEdit4')
        self.cycledayEdit4.setValidator(pIntValidator)

        self.menstrualstartEdit5 = QDateEdit()
        self.menstrualstartEdit5.setObjectName('menstrualstartEdit5')
        self.menstrualstartEdit5.setDateTime(QDateTime.currentDateTime())

        self.menstrualdayEdit5 = QLineEdit()
        self.menstrualdayEdit5.setObjectName('menstrualdayEdit5')
        self.menstrualdayEdit5.setValidator(pIntValidator)

        self.cycledayEdit5 = QLineEdit()
        self.cycledayEdit5.setObjectName('cycledayEdit5')
        self.cycledayEdit5.setValidator(pIntValidator)


        self.historicalMenstruationV3btn = QPushButton()
        self.historicalMenstruationV3btn.setObjectName('historicalMenstruationV3btn')

        self.distUnitCb = QComboBox()
        self.distUnitCb.setObjectName('distUnitCb')

        self.weightUnitCb = QComboBox()
        self.weightUnitCb.setObjectName('weightUnitCb')

        self.tempUnitCb = QComboBox()
        self.tempUnitCb.setObjectName('tempUnitCb')

        self.strideEdit = QLineEdit()
        self.strideEdit.setObjectName('strideEdit')
        self.strideEdit.setValidator(LongInterValidator)
        self.strideEdit.setPlaceholderText('步长')

        self.languageCb = QComboBox()
        self.languageCb.setObjectName('languageCb')

        self.hourFormatCb = QComboBox()
        self.hourFormatCb.setObjectName('hourFormatCb')

        self.weekStartDateCb = QComboBox()
        self.weekStartDateCb.setObjectName('weekStartDateCb')

        self.swimPoolUnitCb = QComboBox()
        self.swimPoolUnitCb.setObjectName('swimPoolUnitCb')

        self.setUnitbtn = QPushButton()
        self.setUnitbtn.setObjectName('setUnitbtn')

        self.cmdlayout.addWidget(self.setDateTimeEdit, 1, 0)
        self.cmdlayout.addWidget(self.timeZoneEdit, 1, 1)
        self.cmdlayout.addWidget(self.setTimebtn, 1, 2)
        self.cmdlayout.addWidget(self.onoffcb, 2, 0)
        self.cmdlayout.addWidget(self.menstruallenEdit, 2, 1)
        self.cmdlayout.addWidget(self.menstrualcycleEdit, 2, 2)
        self.cmdlayout.addWidget(self.lastMenstrualEdit, 2, 3)
        self.cmdlayout.addWidget(self.IntervalEdit, 2, 4)
        self.cmdlayout.addWidget(self.beforeEdit, 2, 5)
        self.cmdlayout.addWidget(self.afterEdit, 2, 6)
        self.cmdlayout.addWidget(self.notifyflagcb, 2, 7)
        self.cmdlayout.addWidget(self.setMenstrualV2btn, 2, 8)
        self.cmdlayout.addWidget(self.startdayEdit, 3, 0)
        self.cmdlayout.addWidget(self.ovulationdayEdit, 3, 1)
        self.cmdlayout.addWidget(self.hourEdit, 3, 2)
        self.cmdlayout.addWidget(self.pergnancyBeforeEdit, 3, 3)
        self.cmdlayout.addWidget(self.pergnancyAfterEdit, 3, 4)
        self.cmdlayout.addWidget(self.menstrualendEdit, 3, 5)
        self.cmdlayout.addWidget(self.setMenstrualRemindV2btn, 3, 6)
        self.cmdlayout.addWidget(self.menstrualstartEdit1, 4, 0)
        self.cmdlayout.addWidget(self.menstrualdayEdit1, 4, 1)
        self.cmdlayout.addWidget(self.cycledayEdit1, 4, 2)
        self.cmdlayout.addWidget(self.menstrualstartEdit2, 5, 0)
        self.cmdlayout.addWidget(self.menstrualdayEdit2, 5, 1)
        self.cmdlayout.addWidget(self.cycledayEdit2, 5, 2)
        self.cmdlayout.addWidget(self.menstrualstartEdit3, 6, 0)
        self.cmdlayout.addWidget(self.menstrualdayEdit3, 6, 1)
        self.cmdlayout.addWidget(self.cycledayEdit3, 6, 2)
        self.cmdlayout.addWidget(self.menstrualstartEdit4, 7, 0)
        self.cmdlayout.addWidget(self.menstrualdayEdit4, 7, 1)
        self.cmdlayout.addWidget(self.cycledayEdit4, 7, 2)
        self.cmdlayout.addWidget(self.menstrualstartEdit5, 8, 0)
        self.cmdlayout.addWidget(self.menstrualdayEdit5, 8, 1)
        self.cmdlayout.addWidget(self.cycledayEdit5, 8, 2)
        self.cmdlayout.addWidget(self.historicalMenstruationV3btn, 8, 3)
        self.cmdlayout.addWidget(self.distUnitCb, 9, 0)
        self.cmdlayout.addWidget(self.weightUnitCb, 9, 1)
        self.cmdlayout.addWidget(self.tempUnitCb, 9, 2)
        self.cmdlayout.addWidget(self.strideEdit, 9, 3)
        self.cmdlayout.addWidget(self.languageCb, 9, 4)
        self.cmdlayout.addWidget(self.hourFormatCb, 9, 5)
        self.cmdlayout.addWidget(self.weekStartDateCb, 9, 6)
        self.cmdlayout.addWidget(self.swimPoolUnitCb, 9, 7)
        self.cmdlayout.addWidget(self.setUnitbtn, 9, 8)

        self.resultlayout = QVBoxLayout()
        self.resultEdit = QTextEdit()
        self.resultEdit.setObjectName('resultEdit')
        # self.resultEdit.setEnabled(False)
        self.resultEdit.setFontPointSize(30)

        self.deviceEdit = QLineEdit()
        self.deviceEdit.setObjectName('deviceEdit')

        self.devicebtn = QPushButton()
        self.devicebtn.setObjectName('devicebtn')

        self.sendcmdbtn = QPushButton()
        self.sendcmdbtn.setObjectName('sendcmdbtn')

        self.resultlayout.addWidget(self.resultEdit)
        self.resultlayout.addWidget(self.deviceEdit)
        self.resultlayout.addWidget(self.devicebtn)
        self.resultlayout.addWidget(self.sendcmdbtn)


        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addLayout(self.cmdlayout)
        self.mainLayout.addLayout(self.resultlayout)



        plate.setWindowModality(Qt.ApplicationModal)
        plate.setWindowFlags(Qt.WindowCloseButtonHint)

        self.retranslateUi(plate)
        QtCore.QMetaObject.connectSlotsByName(plate)


    def retranslateUi(self, plate):
        _translate = QtCore.QCoreApplication.translate
        plate.setWindowTitle(_translate('plate', '工具'))
        self.setTimebtn.setText(_translate('plate', '设置时间'))
        # self.timeZoneEdit.setPlaceholderText('8')
        self.onoffcb.addItems(['开', '关'])
        self.notifyflagcb.addItems(['允许通知', '静默通知', '关闭通知'])
        self.setMenstrualV2btn.setText(_translate('plate', '经期设置'))
        self.setMenstrualRemindV2btn.setText(_translate('plate', '经期提醒设置'))
        self.historicalMenstruationV3btn.setText(_translate('plate', '经期的历史数据下发'))
        self.sendcmdbtn.setText(_translate('plate', '发送指令'))
        self.devicebtn.setText(_translate('plate', '连接'))
        self.distUnitCb.addItems(['km', 'mi'])
        self.weightUnitCb.addItems(['kg', 'lb'])
        self.tempUnitCb.addItems(['摄氏度', '华氏度'])
        self.languageCb.addItems(['英文', '中文', '法语', '德语', '意大利语', '西班牙语', '日语',
                                  '波兰语', '捷克语', '罗马尼亚', '立陶苑语', '荷兰语', '斯洛文尼亚语',
                                  '匈牙利语', '俄罗斯语', '乌克兰语', '斯洛伐克语',
                                 '丹麦语', '克罗地亚语', '印尼语', '韩语', '印地语', '葡萄牙语',
                                  '土耳其语', '泰国语', '越南语', '缅甸语', '菲律宾语', '繁体中文',
                                  '希腊语', '阿拉伯语'])
        self.hourFormatCb.addItems(['24时制', '12时制'])
        self.weekStartDateCb.addItems(['周一', '周日', '周六'])
        self.swimPoolUnitCb.addItems(['米', '码'])
        self.setUnitbtn.setText(_translate('plate', '单位设置'))

