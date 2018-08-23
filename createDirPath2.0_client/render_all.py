# coding:utf8
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys

def render_all(inPathFile):
    app = QApplication(sys.argv)
    app.setStyle('windows')
    app.setStyleSheet('QMainWindow {border:0px solid black;background:rgb(255, 255, 255)}')
    mainWindow = QMainWindow()
    mainWindow.setWindowFlags(Qt.WindowStaysOnTopHint)
    dir_path = QFileDialog.getExistingDirectory(mainWindow, "选择您的路径",inPathFile,options=QFileDialog.ReadOnly)
    return dir_path
    sys.exit(app.exec_())


if __name__ == '__main__':
    path = render_all('')
    print(path)