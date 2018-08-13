# coding:utf8
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys

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

if __name__ == '__main__':
    path = render_one(r'\Users\wang\Desktop')
    print(path)