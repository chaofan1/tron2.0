#!/usr/bin/env python2.6
#-*- coding: utf-8 -*-

# Filename: Ui_SlateInfo.py
# Author: XueFeng, Xiangquan
# Created: 2012/07/02/ 13:00
# Latest Modified: 2013/01/08/ 13:00
# Platform: Windows7
# Copyright: Illumina ltd, PTD department, 2012

import os

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from customComboGrp import CustomComboGrp
from customLineEdit import CustomLineEdit

class Ui_SlateInfo(QFrame):
    def __init__(self, parent = None):
        """ Constructor """
        super(Ui_SlateInfo, self).__init__(parent)
        
        self.vboxLayout = QVBoxLayout(self)
        self.vboxLayout.setContentsMargins(5, 2, 5, 2)
        self.vboxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        self.setCombos()
        self.setOutputElems()
        
    def setCombos(self):
        """ """
        self.comboHLayout = QHBoxLayout()
        self.comboHLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.vboxLayout.addLayout(self.comboHLayout)
        # Resolution ComboBox
        self.resCombo = CustomComboGrp('icon','icon/resolutionIcon.png', QSize(28, 28), QSize(100, 24), self)
        self.resCombo.resize(140, 28)
        self.resCombo.addItem("Dailies")        # !v02  Add Dailies pushButton
        self.resCombo.addItem("Original")
        self.resCombo.addItem("Half")
        self.resCombo.addItem("2048*1024")
        self.resCombo.addItem("1920*1080")
        self.resCombo.addItem("1024*778")
        self.resCombo.addItem("1024*512")
        self.resCombo.addItem("960*540")
        self.resCombo.addItem("720*576")
        self.resCombo.addItem("720*480")
        self.resCombo.addItem("640*480")
        self.comboHLayout.addWidget(self.resCombo)

        
    def setOutputElems(self):
        """ """
        self.outputHLayout = QHBoxLayout()
        self.outputHLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.vboxLayout.addLayout(self.outputHLayout)
        
        self.output = CustomLineEdit('icon/outputIcon.png', QSize(28, 28), QSize(600, 24), self)
        self.output.setText('Select Output Path')
        self.outputHLayout.addWidget(self.output)
        
