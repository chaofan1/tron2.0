# coding:utf8
from PyQt4.QtGui import *
import sys


def render_one(inPathFile):
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    filepath = QFileDialog.getOpenFileName(mainWindow, 'open file', inPathFile)
    return filepath
    sys.exit(app.exec_())


def render_all(inPathFile):
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    filepath = QFileDialog.getExistingDirectory(mainWindow, 'open file', inPathFile)
    return filepath
    sys.exit(app.exec_())
