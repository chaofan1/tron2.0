# coding:utf8
from PyQt4.QtGui import *
import sys

app = QApplication(sys.argv)
mainWindow = QMainWindow()
fileOld = QFileDialog.getOpenFileName(mainWindow, 'open file', '')
file_str = str(fileOld)
print fileOld
print file_str
