#!/usr/bin/env python2.6
#-main.py*- coding: utf-8 -*-

# Filename: main.py
# Author: Xiangquan
# Created: 2013/04/24/ 13:00
# Latest Modified: 2013/04/24/ 13:00
# Platform: Ubuntu10.04
# Copyright: Illumina ltd, PTD department, 2012

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from response import Response

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle('windows')
    app.setStyleSheet( 'QMainWindow {border:0px solid black;background:rgb(211, 211, 211)}\
                    QProgressDialog{background:rgb(211,211,211)}\
                    QMessageBox{background:rgb(211,211,211)}\
                    QToolButton {border: 0px solid black;background-color:transparent;background-image:url(:/toolbtn02.png);}\
                    QToolButton:pressed{border: 0px solid black;background-color:transparent;background-image:url(:/toolbtn03.png);}\
                    QListView {background:rgb(255, 255, 255); border:1px solid black}\
                    QPushButton {border: 1px solid black;border-radius:5px; width:50px;height:25px}\
                    QSplitter::handle{image:url(icon/split.png);width:10px}            \
                    ')
    ui = Response()
    sys.exit(app.exec_())


