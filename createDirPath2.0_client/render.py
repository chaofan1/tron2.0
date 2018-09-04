# coding:utf8
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import os


def render_one(inPathFile):
    app = QApplication(sys.argv)
    app.setStyle('windows')
    app.setStyleSheet('QMainWindow {border:0px solid black;background:rgb(255, 255, 255)}')
    mainWindow = QMainWindow()
    mainWindow.setWindowFlags(Qt.WindowStaysOnTopHint)
    filepath = QFileDialog.getOpenFileName(mainWindow, QString(), inPathFile,
                                           '*.* \n*.mov \n*.mp4 \n*.avi \n*.jpg *.jpeg \n%.png \n*.tiff \n*.tga *.dpx \n*.*',
                                           options=QFileDialog.ReadOnly)
    return filepath
    sys.exit(app.exec_())


def render_all(inPathFile):
    app = QApplication(sys.argv)
    app.setStyle('windows')
    app.setStyleSheet('QMainWindow {border:0px solid black;background:rgb(255, 255, 255)}')
    mainWindow = QMainWindow()
    mainWindow.setWindowFlags(Qt.WindowStaysOnTopHint)
    dir_path = QFileDialog.getExistingDirectory(mainWindow, u"选择您的路径",
                                                inPathFile, options=QFileDialog.ReadOnly)
    return dir_path
    sys.exit(app.exec_())


def remind(datadd,file_number):
    app = QApplication(sys.argv)
    if datadd == "True":
        QMessageBox.information(None, 'INFORMATION', file_number+ u'上传成功，请查看Renderbus网站！', QString('OK'))
    elif datadd == 'send':
        QMessageBox.information(None, 'INFORMATION', file_number + u'开始上传，请稍后查看Renderbus网站！', QString('OK'))
    else:
        QMessageBox.information(None, 'INFORMATION', file_number+ u'上传失败,错误信息:'+datadd, QString('OK'))
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


if __name__ == '__main__':
    path = render_one(r'\Users\wang\Desktop')
    print(path)