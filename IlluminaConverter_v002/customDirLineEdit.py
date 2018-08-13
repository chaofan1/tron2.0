#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Filename: customDirLineEdit.py
# Author: XiangQuan
# Created: 2013/04/24
# Latest Modified: 2013/04/24
# Platform: Ubuntu10.04
# Copyright: Illumina ltd, PTD department, 2012

import os
import platform

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from config import Config

class CustomDirLineEdit(QWidget):
    def __init__(self, iconPath, iconSize = QSize(28, 28), lineEditSize = QSize(100, 28), type = 'input', parent = None):
        """Constructor"""
        super(CustomDirLineEdit, self).__init__(parent)
        self.setWindowFlags(Qt.Widget)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.defaultDir = QString(Config.defaultDir)
        self.createLineGrp(iconPath, iconSize, lineEditSize, type)
        
    def createLineGrp(self, iconPath, iconSize, lineEditSize, type):
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
        self.lineEdit.setStyleSheet('background-color:rgb(35,33,34)')
        #self.lineEdit.setFixedSize(lineEditSize)
        self.horizontalLayout.addWidget(self.lineEdit)
        
        self.dirBtn = QPushButton(' Dir ', self)
        self.dirBtn.setFixedSize(60, 28)
        self.horizontalLayout.addWidget(self.dirBtn)
        if type == 'input':
            QObject.connect(self.dirBtn, SIGNAL('released()'), self.on_inputDirBtn_released)
        elif type == 'output':
            QObject.connect(self.dirBtn, SIGNAL('released()'), self.on_outputDirBtn_released)
        elif type == 'dpx':
            QObject.connect(self.dirBtn, SIGNAL('released()'), self.on_dpxDirBtn_released)

    def on_inputDirBtn_released(self):
        """ Open a seqname file"""
        content = self.textStr()
        if content != '' and content is not None:
            dir = os.path.dirname(content)
            if dir != '':
                self.defaultDir = dir
        (seqname, ext) = QFileDialog.getOpenFileNameAndFilter(None, QString('Open a Sequence'), self.defaultDir, Config.OPENEXTS, options = QFileDialog.ReadOnly)
        path = os.path.dirname(seqname.__str__())
        
        if seqname != QString(''):
            split = seqname.split('.')
            seq = split[0] + '.%04d.' + split[-1]
            self.setText(seq)
            self.defaultDir = QString(path)
            Config.defaultDir = QString(path)
            
    def on_outputDirBtn_released(self):
        """ Get a directory"""
        content = self.textStr()
        self.defaultDir = self.getInputPrjDailies(Config.defaultDir)
        dir = QFileDialog.getExistingDirectory (None, QString('Select a Directory'), self.defaultDir, options = QFileDialog.ShowDirsOnly)
        dir +='/'
        if dir != QString(''):
            self.setText(dir)
            self.defaultDir = QString(dir)

    def on_dpxDirBtn_released(self): 
        content = self.textStr()
        if content != '' and content is not None:
            dir = os.path.dirname(content)
            if dir != '':
                self.defaultDir = dir

        (seqname, ext) = QFileDialog.getOpenFileNameAndFilter(None, QString('Open a Sequence'), self.defaultDir, '*.dpx', options = QFileDialog.ReadOnly)
        path = os.path.dirname(seqname.__str__())
        
        if seqname != QString(''):
            self.setText(seqname)
            self.defaultDir = QString(path)
            
    def getInputPrjDailies(self, fullInput):
        fullInput = str(fullInput)
        splits = fullInput.split('/')
        
        if platform.system() == 'Linux':
            outputDefault = '/All'
            if len(splits) >= 3:
                outputDefault = '/' + splits[1] + '/' + splits[2] + '/Dailies/'
        elif platform.system() == 'Windows':
            outputDefault = 'X:/'
            if len(splits) >= 2:
                outputDefault = splits[0] + '/' + splits[1] + '/Dailies'
                
        return outputDefault
        
    def text(self):
        """return QString"""
        content = self.lineEdit.text()
        return content
    
    def textStr(self):
        """return string"""
        content  = self.lineEdit.text().__str__()
        return content
        
    def textUnicode(self):
        """return a unicode string"""
        content = unicode(self.lineEdit.text().__str__())
        return content
        
    def setText(self, qstring):
        """ """
        if platform.system() == 'Windows':
            qstring = qstring.replace('\\', '/')
        self.lineEdit.setText(qstring)
        
if __name__ == '__main__':
    print CustomDirLineEdit.getInputPrj('/All/DRJ/945/12/Stuff/cmp/public/dadfafa/adfa.%04d.jpg')
