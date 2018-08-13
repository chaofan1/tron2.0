# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys


def consumer(filename):
    app = QApplication(sys.argv)
    progressbar = QProgressBar()
    progressbar.setWindowFlags(Qt.WindowStaysOnTopHint)
    progressbar.setWindowTitle(filename)
    progressbar.setGeometry(400, 200, 800, 40)
    blue = '88B0EB'
    style = """
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #%s;
                width: 20px;
            }""" % blue
    progressbar.setStyleSheet(style)
    progressbar.setMinimum(0)
    progressbar.setMaximum(100)
    progressbar.show()

    while True:
        n = yield
        if not n:
            break
        progressbar.setValue(int(n))

    sys.exit(app.exec_())


if __name__ == '__main__':
    num = 100
    consumer('')