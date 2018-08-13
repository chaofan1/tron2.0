#!/usr/bin/env python2.6
#-*- coding: utf-8 -*-

# Filename: customComboGrp.py
# Author: Xiangquan
# Created: 2013/04/24/
# Latest Modified: 2013/04/24/
# Platform: Ubuntu10.04
# Copyright: Illumina ltd, PTD department, 2012

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from config import Config

class CustomComboGrp(QWidget):
    def __init__(self, type, strInfo, strSize, comboSize=QSize(0, 0), parent = None):
        """Constructor"""
        super(CustomComboGrp, self).__init__(parent)
        self.type = type
        if self.type == 'icon':
            self.setupIconCombo(strInfo, strSize, comboSize)
        elif self.type == 'label':
            self.setupLabelCombo(strInfo, strSize, comboSize)
        
    def setupIconCombo(self, iconPath, iconSize, comboSize):
        """ """
        self.hboxLayout = QHBoxLayout(self)
        self.hboxLayout.setContentsMargins(0, 0, 0, 0)
        self.hboxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.icon = QToolButton(self)
        self.icon.setIconSize(iconSize)
        self.icon.setStyleSheet("background-image:url(%s);background-repeat: repeat-n" % iconPath)
        self.icon.setEnabled(False)
        self.hboxLayout.addWidget(self.icon)
        
        self.combo = QComboBox(self)
        self.combo.setFixedSize(comboSize)
        self.combo.setStyleSheet('background-color:rgb(35,33,34)')
        self.hboxLayout.addWidget(self.combo)
        
    def setupLabelCombo(self, labelText, labelWidth, comboSize):
        """ """
        labelPalette = QPalette()
        labelPalette.setColor(QPalette.WindowText, Config.orange)
        self.labelFont = QFont('Arial')
        self.labelFont.setPointSizeF( Config.contentFontSize * Config.scaleFactor)
        self.labelFont.setLetterSpacing(QFont.PercentageSpacing, 120)
        self.label = QLabel(labelText, self)
        self.label.setPalette(labelPalette)
        self.label.setFont(self.labelFont)
        self.label.setLayoutDirection(Qt.RightToLeft)
        self.label.setFixedWidth(labelWidth)
        self.label.setStyleSheet("QLabel{background-color:rgb(51,51,51);border:0px solid black}"  )

        self.formLayout = QFormLayout(self)
        self.formLayout.setObjectName('labelLineEditFormLayout')
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setSpacing(0)
        self.formLayout.setLabelAlignment(Qt.AlignRight)
        self.formLayout.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        self.combo = QComboBox(self)
        self.combo.setFixedSize(comboSize)
        self.combo.setStyleSheet("QComboBox{background-color:rgb(51,51,51);border:0px solid black;color:white;font:normal 16px}\
                            QComboBox::drop-down{border:0px solid red}")
        self.formLayout.addRow(self.label, self.combo)
        
    def addItem(self, item):
        """ add an Item to the combo box"""
        self.combo.addItem(item)
        
    def setEnabled(self, enable):
        """ set the combo box enabled"""
        self.combo.setEnabled(enable)
        
    def setCurrentIndex(self, index):
        """ """
        self.combo.setCurrentIndex(index)
        
    def currentIndex(self):
        """ """
        return self.combo.currentIndex()
        
    def currentText(self):
        """ get the current text of the combo box"""
        return self.combo.currentText()
        
    def textStr(self):
        qstr = self.currentText()
        return qstr.__str__()
        
    def textUnicode(self):
        str = self.textStr()
        return unicode(str)
        
    def enterEvent(self, event):
        """ """
        super(CustomComboGrp, self).enterEvent(event) 
        if self.type == 'label':
            self.combo.setStyleSheet("QComboBox{background-color:rgb(51,51,51);border:0px solid black;color:white;font:normal 16px}")
        
    def leaveEvent(self, event):
        super(CustomComboGrp, self).leaveEvent(event) 
        if self.type == 'label':
            self.combo.setStyleSheet("QComboBox{background-color:rgb(51,51,51);border:0px solid black;color:white;font:normal 16px}\
                                QComboBox::drop-down{border:0px solid red}")
        
        
