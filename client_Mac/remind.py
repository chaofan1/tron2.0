# coding:utf8
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import os


class Remind:
    def __init__(self):
        self.app = QApplication(sys.argv)

    def remind_success(self,file_number):
        QMessageBox.information(None, 'INFORMATION', file_number + u'上传成功，请查看Renderbus网站！', QString('OK'))
        return
        sys.exit(app.exec_())

    def remind_start(self,file_number):
        QMessageBox.information(None, 'INFORMATION', file_number + u'开始上传，请稍后查看Renderbus网站！', QString('OK'))
        return
        sys.exit(app.exec_())

    def remind_fail(self, fail_info, file_number):
        QMessageBox.information(None, 'INFORMATION', file_number + u'上传失败,错误信息:' + fail_info, QString('OK'))
        return
        sys.exit(app.exec_())

    def remind_ask(self):
        re = QMessageBox.question(None, "INFORMATION", u"相同文件已上传,确定重新上传?", QMessageBox.Yes, QMessageBox.No)  ## 弹出询问框
        if re == QMessageBox.No:
            try:
                os._exit(0)
            except:
                print('exit')
        return
        app.exec_()


if __name__ == '__main__':
    Remind().remind_success('')
    Remind().remind_fail('', '')
    Remind().remind_start('')
    Remind().remind_ask()
