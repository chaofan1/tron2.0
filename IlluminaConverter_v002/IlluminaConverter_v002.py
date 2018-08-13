#!/usr/bin/env python2.6
#-*- coding: utf-8 -*-

# Filename: IlluminaConverter_v002.py
# Author: Xiangquan
# Created: 2013/05/21/
# Latest Modified: 2013/05/21/
# Platform: Ubuntu10.04
# Copyright: Illumina ltd, PTD department, 2012

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from response import Response

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle('windows')
    app.setStyleSheet( 'QMainWindow {border:0px solid black;background:rgb(35, 33, 34)}\
                    QProgressDialog{background:rgb(250,250,250)}\
                    QMessageBox{background:rgb(250,250,250)}\
                    QToolButton {border: 0px solid black;background-color:transparent;background-image:url(:/toolbtn02.png);}\
                    QToolButton:pressed{border: 1px solid black;background-color:transparent;background-image:url(:/toolbtn01.png);}\
                    QListView {background:rgb(51,51,51);border:1px solid rgb(230,190,153)}\
                    QPushButton {border: 1px solid rgb(230,190,153);border-radius:5px; width:50px;height:25px}\
                    QSplitter::handle{image:url(icon/split.png);width:10px}            \
                    QLineEdit{border:2px solid rgb(70,70,70)} \
                    QComboBox{border:1px solid rgb(230,190,153)}\
                    QCheckBox{background-color:rgb(35, 33, 34)}\
                    ')
    ui = Response()
    sys.exit(app.exec_())


