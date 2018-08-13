#!/usr/bin/env python2.6
#-*- coding: utf-8 -*-

# Filename: slate.py
# Author: Xiangquan
# Created: 2013/04/28/
# Latest Modified: 2013/04/28/
# Platform: Windows7
# Copyright: Illumina ltd, PTD department, 2012

import os,  sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from dirAnalyse import DirAnalyse

import Image        #, ImageEnhance

class Slate(object):
    def __init__(self, dirAnalyse, lut, handles, status, date, description, feedback):
        """ Constructor """
        self.dirAnalyse =dirAnalyse
        self.lut = lut
        self.handles = handles
        self.status = status
        self.date = date
        self.description = description
        self.feedback = feedback
        
    @staticmethod
    def createThumbnail(originImgPath, imgSize):
#    def createThumbnail(self, originImgPath, imgSize):
        """ """
        thumbnail = QPixmap(originImgPath)
        tbSize = thumbnail.size()
        originRadio = imgSize.width() * 1.0 / imgSize.height()            # assume originRadio = 16 / 9 = 1.777
        radio = tbSize.width() * 1.0 / tbSize.height()
        
        thumbnailImg = QImage(imgSize,  QImage.Format_ARGB32_Premultiplied)
        painter = QPainter()
        painter.begin(thumbnailImg) 
        painter.fillRect(0, 0, imgSize.width(), imgSize.height(), QColor(0, 0, 0))
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        
        if radio  < originRadio:
            thumbnail = thumbnail.scaledToHeight(imgSize.height(), Qt.SmoothTransformation)
            newTbW= thumbnail.size().width()
            startX = (imgSize.width() - newTbW) / 2
            painter.drawPixmap(startX, 0, thumbnail)
        else:
            thumbnail = thumbnail.scaledToWidth(imgSize.width(), Qt.SmoothTransformation)
            newTbH = thumbnail.size().height()
            startY = (imgSize.height() - newTbH) / 2
            painter.drawPixmap(0, startY, thumbnail)
            
        painter.end()
#        thumbnailImg.save(QString('/JGHome/xiangquan/oiio_test/thumbnail.jpg'))
        return thumbnailImg
        
    
    @staticmethod
    def drawBgTemplate(grayImg, colorImg, size, painter):
        """ """
        
        painter.fillRect(0, 0, size.width(), size.height(), QColor(0, 0, 0))
        gray = QPixmap(grayImg)
        grayW = gray.width()
        gray = gray.scaled(grayW, size.height())
        painter.drawPixmap(0, 0, gray)
        
        color = QPixmap(colorImg)
        colorW = color.width()
        color = color.scaled(colorW, size.height())
        painter.drawPixmap(size.width() - colorW, 0, color)
        
        logo = QPixmap('/JGHome/xiangquan/oiio_test/logo_s.png')
        logoW = logo.width()
        logo = logo.scaledToWidth(logoW * 0.8, Qt.SmoothTransformation)
        painter.drawPixmap(grayW + 30, 40, logo)
        painter.drawImage(size.width() - 230 - 60 , 40, thumbnailImg)
        
        return painter
        
    @staticmethod
    def setFont(family = 'Sans', letterSize = 12, stretchFactor = 100, letterspacing = 2, weight = 50, 
                        bold = False, italic = False, underline = False):
        """ """
        font = QFont(family)
        font.setPointSize(letterSize)
        
        font.setBold(bold)
        font.setWeight(weight)
        font.setItalic(italic)
        font.setUnderline(underline)
        
        font.setStretch(stretchFactor)
        font.setLetterSpacing(QFont.AbsoluteSpacing, letterspacing)
        
        return font
        
    @staticmethod
    def drawText(text, font, color, textX, textY, painter):
        """ """
        painter.setFont(font)
        painter.setPen(color)
        painter.drawText(textX, textY, text)
        
        return painter
        
    @staticmethod
    def drawOutline(thumbnailImg, size, painter):
#    def drawOutline(self, thumbnailImg, shotImg):
        """ """
        painter = Slate.drawBgTemplate('/JGHome/xiangquan/eric/IlluminaConverter/doc/design/gray_measure.jpg', 
                                                            '/JGHome/xiangquan/eric/IlluminaConverter/doc/design/color_measure.jpg', 
                                                            size, painter)

        letterSize = 9
        text = 'www.illuminafx.com'
        textSize = len(text) * letterSize
        textX = (size.width() - textSize) / 2
        textY = size.height() - letterSize - 5
        font = Slate.setFont(painter.font().family(), letterSize, 100, 2, weight = 50)
        painter = Slate.drawText(text, font, QColor(247, 148, 30), textX, textY, painter)

        return painter
        
    @staticmethod
    def drawTitle(size, title, version, titleSize, verSize, painter):
        font = Slate.setFont(painter.font().family(), titleSize, 100, 2, weight = 100, bold = True)
        titleTxtSize = len(title) * titleSize
        titleX = (size.width() - titleTxtSize) / 2
        titleY = titleSize + 60 
        painter = Slate.drawText(title, font, QColor(247, 148, 30), titleX, titleY, painter)
        
        font = Slate.setFont(painter.font().family(), verSize, 100, 2, weight = 50, bold = False)
        verTxtSize = len(version) * verSize
        verX = (size.width() - verTxtSize) / 2
        verY = verSize + titleY + 10
        painter = Slate.drawText(version, font, QColor(247, 148, 30), verX, verY, painter)
        
        return painter
        
    @staticmethod
    def drawSlate(thumbnailImg, shotImg):
        """ """
        imShot = Image.open(shotImg)
        size =  QSize(imShot.size[0], imShot.size[1])
        
        saveImg = QImage(size, QImage.Format_ARGB32_Premultiplied)
        painter = QPainter()
        painter.begin(saveImg)
        
        painter = Slate.drawOutline(thumbnailImg, size, painter)
        painter = Slate.drawTitle(size, 'wlt00101', 'v001_01', 26, 16, painter)

        painter.end()
        saveImg.save(QString('/JGHome/xiangquan/oiio_test/slate.jpg'), 'jpg', quality = 100)
        
        
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    input = '/All/DRJ/038/00/Stuff/efx/img/flip/drj03800_efx_liubj_connectFlip_v001_04/drj03800_efx_liubj_connectFlip_v001_04.$F4.jpg'
    dirAnalyse = DirAnalyse(input)

    thumbnailImg = Slate.createThumbnail('/JGHome/xiangquan/oiio_test/131.png', QSize(224, 126))
    shotImg =  '/All/DRJ/038/00/Stuff/efx/img/flip/drj03800_efx_liubj_connectFlip_v001_04/drj03800_efx_liubj_connectFlip_v001_04.0101.jpg'
    Slate.drawSlate(thumbnailImg, shotImg)
    
    sys.exit(app.exec_())


