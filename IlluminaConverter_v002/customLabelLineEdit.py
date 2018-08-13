#!/usr/bin/env python2.6
#-*- coding: utf-8 -*-

# Filename: customLabelLineEdit.py
# Author:  Xiangquan
# Created: 2013/05/06/
# Latest Modified: 2013/05/06/
# Platform: Ubuntu10.04
# Copyright: Illumina ltd, PTD department, 2012

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from config import Config

class CustomLabelLineEdit(QWidget):
    def __init__(self, labelText = '', fixedWidth = 100,  parent = None):
        """ Constructor """
        super(CustomLabelLineEdit, self).__init__(parent)
        
        self.setWindowFlags(Qt.Widget)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.createLineGrp(labelText, fixedWidth)
        
    def createLineGrp(self, labelText, fixedWidth):
        """ A lable + a lineEdit in a hboxLayout """ 
        labelPalette = QPalette()
        labelPalette.setColor(QPalette.WindowText, Config.orange)
        self.labelFont = QFont('Arial')
        self.labelFont.setPointSizeF( Config.contentFontSize * Config.scaleFactor)
        self.labelFont.setLetterSpacing(QFont.PercentageSpacing, 120)
        self.label = QLabel(labelText, self)
        self.label.setPalette(labelPalette)
        self.label.setFont(self.labelFont)
        self.label.setLayoutDirection(Qt.RightToLeft)
        self.label.setFixedWidth(fixedWidth)
        self.label.setStyleSheet("background-color:rgb(51,51,51);background-repeat: repeat-n; border:0px solid black"  )

        self.formLayout = QFormLayout(self)
        self.formLayout.setObjectName('labelLineEditFormLayout')
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setSpacing(2)
        self.formLayout.setLabelAlignment(Qt.AlignRight)
        self.formLayout.setFormAlignment(Qt.AlignHCenter | Qt.AlignTop)
        
        self.lineEditFont = QFont('Arial')
        self.lineEditFont.setPointSizeF( Config.contentFontSize * Config.scaleFactor)
        self.lineEditFont.setLetterSpacing(QFont.PercentageSpacing, 110)
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setFont(self.lineEditFont)
        self.lineEdit.setObjectName('lineEdit')
        self.lineEdit.setLayoutDirection(Qt.LeftToRight)
        self.lineEdit.setStyleSheet('background-color:rgb(51,51,51);border:0px solid black; color:white')
        self.formLayout.addRow(self.label, self.lineEdit)
        
    def paintEvent(self, paintEvent):
        """ """
        self.lineEditFont.setPointSizeF(Config.contentFontSize * Config.scaleFactor)
        self.lineEdit.setFont(self.lineEditFont)
        
        super(CustomLabelLineEdit, self).paintEvent(paintEvent)
        
    def text(self):
        """return a QString"""
        content = self.lineEdit.text()
        return content
    
    def textStr(self):
        """return a string"""
        content  = self.lineEdit.text().__str__()
        return content
        
    def textUnicode(self):
        """return a unicode string"""
        content = unicode(self.lineEdit.text().__str__())
        return content
        
    def setText(self, qstring):
        """ set a text to the lineEdit"""
        self.lineEdit.setText(qstring)
        
        
        
