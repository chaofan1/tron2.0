#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Filename: customLineEdit.py
# Author: XiangQuan
# Created: 2013/04/24
# Latest Modified: 2013/04/24
# Platform: Ubuntu10.04
# Copyright: Illumina ltd, PTD department, 2012

from PyQt4.QtGui import *
from PyQt4.QtCore import *

class CustomLineEdit(QWidget):
    def __init__(self, iconPath, iconSize = QSize(28, 28), lineEditSize = QSize(100, 28), parent = None):
        """Constructor"""
        super(CustomLineEdit, self).__init__(parent)
        
        self.setWindowFlags(Qt.Widget)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.createLineGrp(iconPath, iconSize, lineEditSize)
        
    def createLineGrp(self, iconPath, iconSize, lineEditSize):
        """ A lable + a lineEdit in a hboxLayout """ 
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setObjectName('customLineHLayout') 
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        
        self.logoBtn = QToolButton(self)
        self.logoBtn.setStyleSheet("background-image:url(%s);background-repeat: repeat-n" % iconPath)
        self.logoBtn.setIconSize(iconSize)
        self.logoBtn.setFocusPolicy(0)
        self.horizontalLayout.addWidget(self.logoBtn)
        
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setObjectName('lineEdit')
        self.lineEdit.setLayoutDirection(Qt.LeftToRight)
        self.lineEdit.setEchoMode( QLineEdit.Normal)
        self.lineEdit.setStyleSheet('background-color:rgb(255,255,255)')
#        self.lineEdit.setFixedSize(lineEditSize)
        self.horizontalLayout.addWidget(self.lineEdit)
        
    def text(self):
        """return QString"""
        content = self.lineEdit.text()
        return content
    
    def textStr(self):
        """return string"""
        content  = self.lineEdit.text().__str__()
        return content
        
    def setText(self, qstring):
        """ """
        self.lineEdit.setText(qstring)
        
#    def setMaxLength(self, length):
#        """ """
#        self.lineEdit.setMaxLength(length)
#    
#    def setValidator(self, validator):
#        """ """
#        self.lineEdit.setValidator(validator)
#        
#    def setCompleter(self, completer):
#        """ """
#        self.lineEdit.setCompleter(completer)
