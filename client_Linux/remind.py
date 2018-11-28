# coding:utf8
from PyQt4.QtGui import *
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')

class Remind:
    def __init__(self):
        self.app = QApplication(sys.argv)

    def remind_success(self,file_number):
        QMessageBox.information(None, 'INFORMATION', file_number + u'上传成功，请查看Renderbus网站！')
        return
        sys.exit(app.exec_())

    def remind_start(self,file_number):
        QMessageBox.information(None, 'INFORMATION', file_number + u'开始上传，请稍后查看Renderbus网站！')
        return
        sys.exit(app.exec_())

    def remind_fail(self, fail_info, file_number):
        QMessageBox.information(None, 'INFORMATION', file_number + u'上传失败,错误信息:' + fail_info)
        return
        sys.exit(app.exec_())

    def download_success(self):
        QMessageBox.information(None, 'INFORMATION', u'下载成功！')
        return
        sys.exit(self.app.exec_())

    def download_fail(self):
        QMessageBox.information(None, 'INFORMATION', u'下载失败！')
        return
        sys.exit(self.app.exec_())

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
    # Remind().remind_fail('', '')
    # Remind().remind_start('')
    # Remind().remind_ask()