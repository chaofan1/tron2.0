# coding:utf8
from PyQt4.QtGui import *
import sys


class Render:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.mainWindow = QMainWindow()

    def render_one(self,inPathFile):
        filepath = QFileDialog.getOpenFileName(self.mainWindow, 'open file', inPathFile)
        return filepath
        sys.exit(self.app.exec_())

    def render_all(self,inPathFile):
        filepath = QFileDialog.getExistingDirectory(self.mainWindow, 'open file', inPathFile)
        return filepath
        sys.exit(self.app.exec_())


if __name__ == '__main__':
    p = Render().render_all('')
    print p
    p2 = Render().render_one('')
    print p2
