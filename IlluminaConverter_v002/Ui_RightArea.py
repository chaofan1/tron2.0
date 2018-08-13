#!/usr/bin/env python2.6
#-*- coding: utf-8 -*-

# Filename: Ui_LeftArea.py
# Author: Xiangquan
# Created: 2013/04/24/
# Latest Modified: 2013/04/24/
# Platform: Ubuntu10.04
# Copyright: Illumina ltd, PTD department, 2012

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from Ui_InputList import Ui_InputList
from Ui_SlateInfo import Ui_SlateInfo

class Ui_RightArea(QFrame):
    def __init__(self, parent = None):
        """ """
        super(Ui_RightArea, self).__init__(parent)
        self.vLayout = QVBoxLayout(self)
        self.vLayout.setAlignment(Qt.AlignRight | Qt.AlignTop)
        self.vLayout.setContentsMargins(0, 0, 10, 0)
        self.vLayout.setSpacing(10)
        
        self.__setInputList__()
        self.__setSlateInfo__()
        
    def __setInputList__(self):
        self.inputList = Ui_InputList(self)
        self.vLayout.addWidget(self.inputList)
        
    def __setSlateInfo__(self):
        """ Connet Ui_SlateInfo Setting"""
        self.slateInfo = Ui_SlateInfo(self)
        self.vLayout.addWidget(self.slateInfo)
        
        
        
