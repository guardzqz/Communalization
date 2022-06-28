import uiautomator2 as u2
import os
import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMessageBox, QCheckBox

from UI.menstrualUI import MenstrualUI
from ble.comFunc import comFunc
from ble.menstrual import menstrual


class MenView(QDialog, MenstrualUI):
    def __init__(self):
        super(MenView, self).__init__()
        self.setupUi(self)
        self.device = None

    @QtCore.pyqtSlot()
    def on_devicebtn_clicked(self):
        hh = self.deviceEdit.text()
        if hh:
            try:
                self.device = u2.connect(hh.strip())
                print(self.device)
                self.resultEdit.setPlainText('连接成功')
                self.sendcmdbtn.setEnabled(True)
            except Exception as e:
                print(e)
                self.resultEdit.setPlainText(str(e))
                self.sendcmdbtn.setEnabled(False)


    @QtCore.pyqtSlot()
    def on_setTimebtn_clicked(self):
        lastcmd = comFunc.setTime(self.setDateTimeEdit.text(), self.timeZoneEdit.text())
        self.resultEdit.setPlainText(lastcmd)

    @QtCore.pyqtSlot()
    def on_sendcmdbtn_clicked(self):
        text = self.resultEdit.toPlainText()
        if '-' in text and self.device:
            self.device(resourceId='test.com.ido:id/custom_cmd_data_et').clear_text()
            self.device(resourceId='test.com.ido:id/custom_cmd_data_et').set_text(text)
            self.device.press('back')
            self.device(text='发送自定义命令').click()

    @QtCore.pyqtSlot()
    def on_setMenstrualV2btn_clicked(self):
        textlist = [self.menstruallenEdit,self.menstrualcycleEdit, self.IntervalEdit,self.beforeEdit,self.afterEdit]
        default = [7, 30, 14, 5, 4]
        for i in range(len(textlist)):
            if not textlist[i].text():
                textlist[i].setText(str(default[i]))
        lastcmd = menstrual.setMenstrualV2([self.onoffcb.currentText(), self.menstruallenEdit.text(),self.menstrualcycleEdit.text(),self.lastMenstrualEdit.text(),
                                 self.IntervalEdit.text(),self.beforeEdit.text(),self.afterEdit.text(), self.notifyflagcb.currentText()])
        print('lastcmd', lastcmd)
        self.resultEdit.setPlainText(lastcmd)

    @QtCore.pyqtSlot()
    def on_setMenstrualRemindV2btn_clicked(self):
        print(self.ovulationdayEdit,self.hourEdit,self.pergnancyBeforeEdit, self.pergnancyAfterEdit, self.menstrualendEdit)
        textlist = [self.startdayEdit, self.ovulationdayEdit,self.hourEdit,self.pergnancyBeforeEdit, self.pergnancyAfterEdit, self.menstrualendEdit]
        default = [3, 3, 20, 3, 3, 3]
        for i in range(len(textlist)):
            print(default[i], textlist[i].text())
            if not textlist[i].text():
                textlist[i].setText(str(default[i]))
            default[i] = textlist[i].text()

        lastcmd = menstrual.setMenstrualRemindV2(default)
        self.resultEdit.setPlainText(lastcmd)

    @QtCore.pyqtSlot()
    def on_historicalMenstruationV3btn_clicked(self):
        data = []
        textlist = ['menstrualstartEdit', 'menstrualdayEdit', 'cycledayEdit']
        for t in range(1, 6):
            print(getattr(self, textlist[0]+str(t)).text())
            if not getattr(self, textlist[1]+str(t)).text() or not getattr(self, textlist[2]+str(t)).text():
                continue
            data.append([getattr(self, textlist[0]+str(t)).text(), getattr(self, textlist[1]+str(t)).text(), getattr(self, textlist[2]+str(t)).text()])
        lastcmd = menstrual.historicalMenstruationV3(data)
        self.resultEdit.setPlainText(lastcmd)

    @QtCore.pyqtSlot()
    def on_setUnitbtn_clicked(self):
        if not self.strideEdit.text():
            self.strideEdit.setText('90')
        lastcmd = comFunc.setUnit([self.distUnitCb.currentText(), self.weightUnitCb.currentText(), self.tempUnitCb.currentText(),
                         self.strideEdit.text(), self.languageCb.currentText(), self.hourFormatCb.currentText(),
                         self.weekStartDateCb.currentText(), self.swimPoolUnitCb.currentText()])
        self.resultEdit.setPlainText(lastcmd)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = MenView()
    # style = CommonHelper.readQss(r'style/mainView.qss')
    # demo.setStyleSheet(style)
    demo.show()
    sys.exit(app.exec())
