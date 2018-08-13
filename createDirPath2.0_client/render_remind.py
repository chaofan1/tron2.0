#coding:utf-8
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import os


def remind(datadd):
    app = QApplication(sys.argv)
    if datadd is "True":
        QMessageBox.information(None, 'INFORMATION', u'文件上传成功，请稍后查看Renderbus网站！', QString('OK'))
    else:
        QMessageBox.information(None, 'INFORMATION', u'上传失败！', QString('OK'))
    return
    sys.exit(app.exec_())


def ask():
    app = QApplication(sys.argv)
    re = QMessageBox.question(None, "INFORMATION", u"相同文件已上传,确定重新上传?", QMessageBox.Yes, QMessageBox.No)  ## 弹出询问框
    if re == QMessageBox.No:
        try:
            os._exit(0)
        except:
            print('exit')
    return
    app.exec_()