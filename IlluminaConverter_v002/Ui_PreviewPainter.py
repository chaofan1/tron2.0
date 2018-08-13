#!/usr/bin/env python2.6
#-*- coding: utf-8 -*-

# Filename: Ui_PreviewPainter.py
# Author:  Xiangquan
# Created: 2013/04/24/
# Latest Modified: 2013/05/06/
# Platform: Ubuntu10.04
# Copyright: Illumina ltd, PTD department, 2012

import os.path
import math
import platform

from PIL import Image
from PIL import ImageEnhance

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from dirAnalyse import DirAnalyse
from customLabelLineEdit import CustomLabelLineEdit
from customComboGrp import CustomComboGrp
from customTextEdit import CustomTextEdit
from fnImgHandle import FnImgHandle

from config import Config

class Ui_PreviewPainter(QFrame):
    def __init__(self, parent = None):
        """ Constructor"""
        super(Ui_PreviewPainter, self).__init__(parent)
        self.setMinimumSize(960, 540)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.vboxLayout = QVBoxLayout(self)
        self.vboxLayout.setAlignment(Qt.AlignTop)
        self.vboxLayout.setSpacing(0)
        self.setGridItems()
        self.setTextEdits()
        
        self.bg = QPixmap(Config.slateBG)
        self.oldWidgetSize = self.bg.size()
        
        self.transferInfo = parent.transferInfo
        self.input = self.transferInfo.input
        self.dpxtc = self.transferInfo.dpxtc
        self.dirAnalyse = None
        self.title = QString('')
        self.ver = QString('')                      #self.ver = QString('v001_15')
        
    def setGridItems(self):
        """ """
        self.itemsVLayout = QVBoxLayout()
        self.itemsVLayout.setAlignment(Qt.AlignTop)
        self.itemsVLayout.setSpacing(0)
        self.vboxLayout.addLayout(self.itemsVLayout)
        
        self.itemsGridLayout = QGridLayout()
        self.itemsGridLayout.setAlignment(Qt.AlignTop)
        self.itemsGridLayout.setContentsMargins(0, 0, 0, 0)
        self.itemsGridLayout.setSpacing(0)
        self.itemsVLayout.addLayout(self.itemsGridLayout)
        
        self.setGridLeftItems()
        self.setGridRightItems()
        
    def setGridLeftItems(self):
        """ """
        if platform.system() == 'Linux':
            self.vfxcode = CustomLabelLineEdit(':VFX Code')
            self.shot = CustomLabelLineEdit(':Shot')        
            self.duration = CustomLabelLineEdit(':Duration')        
            self.handles = CustomLabelLineEdit(':Handles')        
            self.timecode = CustomLabelLineEdit(':Time Code')
            self.status = CustomComboGrp('label',':Status', 100, QSize(180, 24))
            self.date = CustomLabelLineEdit(':Date')
            
        elif platform.system() == 'Windows':
            self.vfxcode = CustomLabelLineEdit(' VFX Code:')
            self.shot = CustomLabelLineEdit('           Shot:')
            self.duration = CustomLabelLineEdit('     Duration:')
            self.handles = CustomLabelLineEdit('     Handles:')
            self.timecode = CustomLabelLineEdit('Time Code:')
            self.status = CustomComboGrp('label','        Status:', 100, QSize(180, 24))
            self.date = CustomLabelLineEdit('           Date:')
        elif platform.system() == 'Darwin':
            self.vfxcode = CustomLabelLineEdit(' VFX Code:')
            self.shot = CustomLabelLineEdit('           Shot:')
            self.duration = CustomLabelLineEdit('     Duration:')
            self.handles = CustomLabelLineEdit('     Handles:')
            self.timecode = CustomLabelLineEdit('Time Code:')
            self.status = CustomComboGrp('label','        Status:', 100, QSize(180, 24))
            self.date = CustomLabelLineEdit('           Date:')
        
        self.itemsGridLayout.addWidget(self.vfxcode, 0, 0)
        self.itemsGridLayout.addWidget(self.shot, 1, 0)
        self.itemsGridLayout.addWidget(self.duration, 2, 0)
        self.itemsGridLayout.addWidget(self.handles, 3, 0)
        self.itemsGridLayout.addWidget(self.timecode, 4, 0)
        
        for item in Config.status:
            self.status.addItem(item)
        self.itemsGridLayout.addWidget(self.status, 5, 0)
        
        self.itemsGridLayout.addWidget(self.date, 6, 0)
        
    def setGridRightItems(self):
        """ """
        if platform.system() == 'Linux':
            self.lut = CustomComboGrp('label',':LUT', 120, QSize(150, 24))
            self.maskRatio = CustomComboGrp('label',':Mask Ratio', 120, QSize(150, 24))
            self.resolution = CustomLabelLineEdit(':Resolution', 120)
            self.format = CustomLabelLineEdit(':Format', 120)
            
        elif platform.system() == 'Windows':
            self.lut = CustomComboGrp('label','                 LUT:', 120, QSize(150, 24))
            self.maskRatio = CustomComboGrp('label','    Mask Ratio:', 120, QSize(150, 24))
            self.resolution = CustomLabelLineEdit('     Resolution:', 120)
            self.format = CustomLabelLineEdit('           Format:', 120)

        elif platform.system() == 'Darwin':
            self.lut = CustomComboGrp('label', ':LUT', 120, QSize(150, 24))
            self.maskRatio = CustomComboGrp('label', ':Mask Ratio', 120, QSize(150, 24))
            self.resolution = CustomLabelLineEdit(':Resolution', 120)
            self.format = CustomLabelLineEdit(':Format', 120)
        for item in Config.lut:
            self.lut.addItem(item)
        self.itemsGridLayout.addWidget(self.lut, 3, 1)
        
        for item in Config.maskRatio:
            self.maskRatio.addItem(item)
        self.itemsGridLayout.addWidget(self.maskRatio, 4, 1)

        self.itemsGridLayout.addWidget(self.resolution, 5, 1)
        self.itemsGridLayout.addWidget(self.format, 6, 1)        
        
    def setTextEdits(self):
        """ """
        self.textEditHLayout = QHBoxLayout()
        self.textEditHLayout.setSpacing(20)
        self.textEditHLayout.setContentsMargins(0, 0, 0, 0)
        self.vboxLayout.addLayout(self.textEditHLayout)
        
        self.description = CustomTextEdit('Description')
        self.textEditHLayout.addWidget(self.description)
        
        self.feedback = CustomTextEdit('Feedback')
        self.textEditHLayout.addWidget(self.feedback)
        
    def paintEvent(self, event):
        """ """
        painter = QPainter()
        painter.begin(self) 

        if platform.system() == 'Linux':
            if  Config.repaint != 2:
                self.paintSlateContent(painter, self.dirAnalyse)
        elif platform.system() == 'Windows':
            self.paintSlateContent(painter, self.dirAnalyse)      
        
        painter.end()
        super(Ui_PreviewPainter, self).paintEvent(event)
        
    def paintSlateContent(self, painter, dirAnalyse):
        """ """
        widgetSize = self.size()
        scaleW = self.oldWidgetSize.width() * 1.0 / widgetSize.width()
        scaleH = self.oldWidgetSize.height() * 1.0/ widgetSize.height()
        ratio = widgetSize.width() * 1.0 / widgetSize.height()

        #background        
        painter.fillRect(0, 0, widgetSize.width(), widgetSize.height(), QColor(0, 0, 0))
        bg = QPixmap(Config.slateBG)
        bgSize = bg.size()
        if ratio  < Config.originRatio:                        #assume ratio = 4 / 002 = 1.333
            bg = bg.scaledToWidth(widgetSize.width(), Qt.SmoothTransformation)
            bgH = bg.size().height()
            x = 0
            y = (widgetSize.height() - bgH) / 2.0
            Config.scaleFactor = bg.size().width() * 1.000 / bgSize.width()
        else:
            bg = bg.scaledToHeight(widgetSize.height(), Qt.SmoothTransformation)
            bgW = bg.size().width()
            x = (widgetSize.width() - bgW) / 2.0
            y = 0
            Config.scaleFactor = bg.size().height() * 1.000 / bgSize.height()
        painter.drawPixmap(x, y, bg)
        
        #title
        painter.setPen(Config.orange)
        if dirAnalyse is not None:
            self.title = QString(dirAnalyse.titlename) 
        else:
            self.title = QString(' ')
        titleLen = self.title.size()
        titleFontSize = Config.titleFontSize * Config.scaleFactor
        titleFont = QFont('Arial')
        titleFont.setPointSizeF(titleFontSize)
        if platform.system() == 'Linux':
            titleFont.setWeight(56) 
        elif platform.system() == 'Windows':
            titleFont.setWeight(70)
        titleFont.setLetterSpacing(QFont.PercentageSpacing, 102)
        painter.setFont(titleFont)
        titlex = (widgetSize.width() - titleFontSize * titleLen * 0.75) * 1.0 / 2
        y = y + Config.titleDist * Config.scaleFactor
        painter.drawText(titlex, y, self.title)
        
        #thumbnail
        if dirAnalyse is not None and dirAnalyse.files  != [] :
            tbSize = Config.basicTbSize * 0.5
            tbX = widgetSize.width() - tbSize.width() - 56
            tbY = y - Config.titleFontSize
            painter.fillRect(tbX, tbY, tbSize.width() , tbSize.height(), QColor(0, 0, 0))
            if dirAnalyse.files[0].split('.')[-1] not in Config.TOJPG:
                originImg = QPixmap(os.path.join(dirAnalyse.path, dirAnalyse.files[0]))
            else:
                if platform.system() == 'Linux':
                    basePath = os.environ['HOME']
                elif platform.system() == 'Windows':
                    basePath = 'D:/'
                    
                tbImg =  os.path.join(basePath, '.thumbnail.jpg')
                FnImgHandle.convertImgToJpg(os.path.join(dirAnalyse.path, dirAnalyse.files[0]), tbImg)
                originImg = QPixmap(tbImg)
                dirAnalyse.resolution = dirAnalyse.getResolution(basePath, '.thumbnail.jpg')
                self.resolution.setText(dirAnalyse.resolution)

            startX, startY, tbPixmap = FnImgHandle. scaleImage(originImg, tbSize)
            painter.drawPixmap(tbX + startX, tbY + startY, tbPixmap)
        
        #version
        painter.setPen(Config.white)
        if dirAnalyse is not None:
            self.ver = QString(dirAnalyse.version)
        else:
            self.ver = QString(' ')
        verLen = self.ver.size()
        verFontSize = Config.verFontSize * Config.scaleFactor
        verFont = QFont('Arial')
        verFont.setPointSizeF(verFontSize)
        verFont.setWeight(50)
        verFont.setLetterSpacing(QFont.PercentageSpacing, 100)
        painter.setFont(verFont)
        verx = (widgetSize.width() - verFontSize * verLen * 0.7) * 1.0 / 2
        y = y + Config.titleToVer * Config.scaleFactor
        painter.drawText(verx, y, self.ver)

        #items
        top = y + Config.optionToVer * Config.scaleFactor * 0.2
        left = x + Config.optionToLeft * Config.scaleFactor
        right = x + Config.optionToRight * Config.scaleFactor
        bottom = Config.optiontoTextEdit * Config.scaleFactor
        self.itemsVLayout.setContentsMargins(left, top, right, bottom)
        spacing = Config.optionSpacing * Config.scaleFactor * 0.3
        self.itemsGridLayout.setSpacing(spacing)
        
        Config.repaint += 1
        
        


