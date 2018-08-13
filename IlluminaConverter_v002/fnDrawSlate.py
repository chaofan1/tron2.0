#!/usr/bin/env python2.6
#-*- coding: utf-8 -*-

# Filename: fnDrawSlate.py
# Author:  Xiangquan
# Created: 2013/05/09/
# Latest Modified: 2013/05/09/
# Platform: Ubuntu10.04
# Copyright: Illumina ltd, PTD department, 2012

import os
import math
import platform

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from config import Config
from fnImgHandle import FnImgHandle

class FnDrawSlate(object):
    def __init__(self, title, ver):
        """ Constructor"""
        self.title = title
        self.ver = ver
        
    def saveSlate(self, imgSize, tbImgPath, outputfile, slateInfo):
        """
        imgSize: the  size of sequence image 
        outputfile: the full path of saving the slate     
        """
        running = True
        #if  draw Slate:
        if Config.drawSlate:
            try:
                #HD basic slate image
                slateImg = QImage(Config.basicSlateSize,  QImage.Format_ARGB32_Premultiplied)
                slPainter = QPainter()
                slPainter.begin(slateImg) 
                self.drawSlate(slPainter, tbImgPath, Config.basicSlateSize, Config.basicTbSize, slateInfo )
                slPainter.end()

                #the final slate to the sequence
                bgImg = QImage(imgSize,  QImage.Format_ARGB32_Premultiplied)
                bgPainter = QPainter()
                bgPainter.begin(bgImg)
                bgPainter.fillRect(0, 0, imgSize.width(), imgSize.height(), QColor(0, 0, 0))
                startX, startY, slateImg = FnImgHandle.scaleImage(slateImg, imgSize)
                bgPainter.drawImage(startX, startY, slateImg)
                bgPainter.end()
                bgImg.save(outputfile, quality = 100)
            except Exception, e:
                running = False
                print e
                QMessageBox .critical(None, 'ERROR', u' FnDrawSLate::saveSlate(): %s ' % str(e).decode('utf-8'), QString('OK'))
            
        return running
        
    def drawSlate(self, painter, thumbnailPath, slateSize, tbSize, slateInfo):
        """ """
        bg = QPixmap(Config.realSlate)
        bgSize = bg.size()
        
        painter.drawPixmap(0, 0, bg)
        #title
        painter.setPen(Config.orange);    
        titleLen = self.title.size()
        titleFont = QFont('Arial')
        titleFont.setPointSizeF(Config.titleFontSize)
        if platform.system() == 'Linux':
            titleFont.setWeight(56) 
        elif platform.system() == 'Windows':
            titleFont.setWeight(70)
        titleFont.setLetterSpacing(QFont.PercentageSpacing, 102)
        painter.setFont(titleFont)
        titlex = (slateSize.width() - Config.titleFontSize * titleLen * 0.75) * 1.0 / 2
        y = 0 + Config.titleDist
        painter.drawText(titlex, y, self.title)
        
        #thumbnail
        tbX = slateSize.width() - tbSize.width() - 100
        tbY = y - Config.titleFontSize
        painter.fillRect(tbX, tbY, tbSize.width(), tbSize.height(), QColor(0, 0, 0))
        
        if thumbnailPath.split('.')[-1] not in Config.TOJPG:
            originImg = QPixmap(thumbnailPath)
        else:
            if platform.system() == 'Linux':
                basePath = os.environ['HOME']
            elif platform.system() == 'Windows':
                basePath = 'D:/'
            
            tbImg =  os.path.join(basePath, '.thumbnail2.jpg')
            FnImgHandle.convertImgToJpg(thumbnailPath, tbImg)
            originImg = QPixmap(tbImg)
            
        startX, startY, tbPixmap = FnImgHandle. scaleImage(originImg, tbSize)
        painter.drawPixmap(tbX + startX, tbY + startY, tbPixmap)
        
        #version
        painter.setPen(Config.white)
        verLen = self.ver.size()
        verFontSize = Config.verFontSize
        verFont = QFont('Arial')
        verFont.setPointSizeF(verFontSize)
        verFont.setWeight(50)
        verFont.setLetterSpacing(QFont.PercentageSpacing, 100)
        painter.setFont(verFont)
        verx = (slateSize.width()  - verFontSize * verLen * 0.75) * 1.0 / 2
        y = y + Config.titleToVer
        painter.drawText(verx, y, self.ver)
    
        #content
        painter.setPen(Config.white)
        contentFont = QFont('Arial')
        contentFont.setPixelSize(Config.slateInfoSize)
        painter.setFont(contentFont)

        painter.drawText(365, 165 + 18, slateInfo.vfxcode)                      #        painter.drawText(365, 165 + 18, 'wlt99901')
        painter.drawText(365, 200 + 22, slateInfo.shot)                           #        painter.drawText(365, 200 + 22, '99901')
        painter.drawText(365, 245 + 16, slateInfo.duration)                     #        painter.drawText(365, 245 + 16, '101 - 246')
        painter.drawText(365, 285 + 16, slateInfo.handles)                      #        painter.drawText(365, 285 + 16, '4+4')
        painter.drawText(365, 320 + 20, slateInfo.timecode)                    #        painter.drawText(365, 320 + 20, '21:53:56:03')
        painter.drawText(365, 360 + 18, slateInfo.status)                         #        painter.drawText(365, 360 + 18, 'Final Comp')
        painter.drawText(365, 400 + 16, slateInfo.date)                            #        painter.drawText(365, 400 + 16, '05/05/2013 16:42')
        
        painter.drawText(1155, 285 + 16, slateInfo.lut)                             #        painter.drawText(1155, 285 + 16, 'sRGB')
        painter.drawText(1155, 320 + 20, slateInfo.maskRatio)                 #        painter.drawText(1155, 320 + 20, 'no mask')
        painter.drawText(1155, 360 + 18, slateInfo.resolution)                  #        painter.drawText(1155, 360 + 18, '2200 x 1160')
        painter.drawText(1155, 400 + 16, slateInfo.format)                       #        painter.drawText(1155, 400 + 16, 'dpx')
        
        #description & feedback
        textEditFont = QFont(Config.textFont)
        textEditFont.setPixelSize(Config.textEditSize)
        textEditFont.setLetterSpacing(QFont.PercentageSpacing, 110)
        painter.setFont(textEditFont)
        for descIndex in range(len(slateInfo.description)):
            painter.drawText(145, 526 + 34 * descIndex, unicode(slateInfo.description[descIndex]))

        for fbIndex in range(len(slateInfo.feedback)):
            painter.drawText(1045, 526 + 34 * fbIndex, unicode(slateInfo.feedback[fbIndex]))
        
        
