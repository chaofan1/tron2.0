#!/usr/bin/env python2.6
#-*- coding: utf-8 -*-

# Filename: customTextEdit.py
# Author:  Xiangquan
# Created: 2013/05/06/
# Latest Modified: 2013/05/06/
# Platform: Ubuntu10.04
# Copyright: Illumina ltd, PTD department, 2012

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from config import Config

class CustomTextEdit(QWidget):
    def __init__(self, labelText = '', parent = None):
        """ Constructor """
        super(CustomTextEdit, self).__init__(parent)
        
        self.setWindowFlags(Qt.Widget)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        self.fixedWidth = 450
        self.createColumnGrp(labelText)
        
        textCursor = self.textEdit.textCursor()
        self.oldColumnNum = textCursor.columnNumber()
        self.oldPosition = textCursor.position()
        
        QObject.connect(self.textEdit, SIGNAL('cursorPositionChanged()'), self.cursorPosChanged)
        
    def createColumnGrp(self, labelText):
        """ A lable + a lineEdit in a hboxLayout """ 
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName('customLineHLayout') 
#        self.verticalLayout.setContentsMargins(14, 0, 14, 14)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(5)
        
        labelPalette = QPalette()
        labelPalette.setColor(QPalette.WindowText, Config.textGray)
        self.labelFont = QFont('Arial')
        self.labelFont.setPointSizeF( Config.contentFontSize * Config.scaleFactor)
        self.labelFont.setLetterSpacing(QFont.PercentageSpacing, 110)
        self.label = QLabel(labelText, self)
        self.label.setPalette(labelPalette)
        self.label.setFont(self.labelFont)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background-color:transparent;" )
        self.verticalLayout.addWidget(self.label)
        
        self.textEditFont = QFont(Config.textFont)
        self.textEditFont.setPointSizeF( Config.contentFontSize * Config.scaleFactor *  1.0)
        self.textEdit = QTextEdit(self)
        self.textEdit.setFont(self.textEditFont)
        self.textEdit.setObjectName('lineEdit')
        self.textEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit.setStyleSheet('background:rgb(51,51,51);border:0px solid black; color:white;')
#        self.textEdit.setStyleSheet('background:transparent;border:0px solid black; color:white;')
        self.setFixedSize(QSize(self.fixedWidth, 300))
        self.verticalLayout.addWidget(self.textEdit)
        
    def paintEvent(self, paintEvent):
        """ """
        self.labelFont.setPointSizeF(Config.contentFontSize * Config.scaleFactor)
        self.label.setFont(self.labelFont)
        
        self.textEditFont.setPointSizeF( Config.contentFontSize * Config.scaleFactor * 1.0)
        self.textEdit.setFont(self.textEditFont)
        
        super(CustomTextEdit, self).paintEvent(paintEvent)
        
    def readTextEditLine(self, startPos):
        """ """
        end = False
        textCursor = self.textEdit.textCursor()
        textCursor.setPosition(startPos)
        textCursor.movePosition(QTextCursor.Down, QTextCursor.KeepAnchor)
        endPos = textCursor.position()
        if endPos == startPos:              #if the current line is the last line, redo the text selection
            endPos = textCursor.position()
            textCursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
            end = True
        lineContent = unicode(textCursor.selectedText())
        return end, endPos, lineContent
        
    def readAsList(self):
        """ """
        textEditList = []
        startPos = 0
        end = False
        while  not end:
            end, startPos, lineContent = self.readTextEditLine(startPos)
            textEditList.append(lineContent)
            
        return textEditList
        
    def cursorPosChanged(self):
        """ """
        textCursor = self.textEdit.textCursor()
        block = textCursor.block()
        textLayout = block.layout()
        position = textLayout.position()
        
        columnNum = textCursor.columnNumber()
        
        doc = self.textEdit.document()
        doc.setPageSize(QSizeF(self.fixedWidth, 290.0))

#        if position.y() == 268.0:
#            print 'the end of the page'
        
    def text(self):
        """return QString"""
        content = self.textEdit.text()
        return content
    
    def textStr(self):
        """return string"""
        content  = self.textEdit.text().__str__()
        return content
        
    def setText(self, qstring):
        """ """
        self.textEdit.setText(qstring)
        
