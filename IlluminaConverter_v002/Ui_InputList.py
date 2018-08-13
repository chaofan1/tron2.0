#!/usr/bin/env python2.6
#-*- coding: utf-8 -*-

# Filename: Ui_TransferInfo.py
# Author: XueFeng, Xiangquan
# Created: 2012/07/02/ 13:00
# Latest Modified: 2013/01/08/ 13:00
# Platform: Windows7
# Copyright: Illumina ltd, PTD department, 2012

import os

from PyQt4.QtGui import *
from PyQt4.QtCore import *

class Ui_InputList(QFrame):
    def __init__(self, parent = None):
        """ Constructor"""
        super(Ui_InputList, self).__init__(parent)
        
        
        self.setupUi()
        
    def setupUi(self):
        self.vboxLayout = QVBoxLayout(self)
        self.vboxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.vboxLayout.setContentsMargins(5, 1, 5, 1)
        
        #add & rm btns
        self.setupBtns('icon/addIcon.png', QSize(28, 28), 'icon/removeIcon.png', QSize(28, 28))
        
        # Convert Path list
        self.setupConvertList('icon/none.png')
        
    def setupBtns(self, addIcon, addIconSize, rmIcon, rmIconSize):
        """ """
        self.hboxLayout = QHBoxLayout()
        self.hboxLayout.setAlignment(Qt.AlignRight | Qt.AlignTop)
        self.hboxLayout.setSpacing(20)
        self.vboxLayout.addLayout(self.hboxLayout) 
        
        # Add Path Btn
        self.addBtn = QToolButton(self)
        self.addBtn.setStyleSheet("background-image:url(%s);background-repeat: repeat-n" % addIcon)
        self.addBtn.setIconSize(addIconSize)
        self.addBtn.setFocusPolicy(0)
        self.hboxLayout.addWidget(self.addBtn)
        
        # Delete convert Path
        self.rmBtn = QToolButton(self)
        self.rmBtn.setStyleSheet("background-image:url(%s);background-repeat: repeat-n" % rmIcon)
        self.rmBtn.setIconSize(rmIconSize)
        self.rmBtn.setFocusPolicy(0)
        self.hboxLayout.addWidget(self.rmBtn)
        
    def setupConvertList(self, iconPath):
        """ """
        self.convertVBoxLayout = QVBoxLayout()
        self.convertVBoxLayout.setAlignment(Qt.AlignRight | Qt.AlignTop)
        self.vboxLayout.addLayout(self.convertVBoxLayout)
        
        #Add list widget
        self.convertList = QListWidget(self)
        self.convertList.setStyleSheet("background-image:url(%s)" % iconPath)
        self.convertVBoxLayout.addWidget(self.convertList)
        
        
