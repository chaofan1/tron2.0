#!/usr/bin/env python2.6
#-*- coding: utf-8 -*-

# Filename: fnDrawMask.py
# Author:  Xiangquan
# Created: 2013/05/09/
# Latest Modified: 2013/05/09/
# Platform: Ubuntu10.04
# Copyright: Illumina ltd, PTD department, 2012

import os
import math

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from config import Config
from slateInfo import SlateInfo
from fnImgHandle import FnImgHandle

class FnDrawMask(object):
    def __init__(self):
        """ Constructor"""
        pass
        
    @staticmethod
    def getMask(imgSize, alpha, maskRatio):
        """ """
#        print 'fnDrawMask::getMask:'
#        print  'imgSize:', imgSize
        imgWidth = imgSize.width()
        imgHeight = imgSize.height()
        imgRatio = imgWidth * 1.0 / imgHeight
        direction = 0                       #0: up-bottom; 1: left-right
        if maskRatio > imgRatio:            #e.g, imgRatio = 2200.0/1160 = 1.896, maskRatio = 2.35
            singleMaskHeight = (imgHeight - imgWidth / maskRatio) / 2
            maskSize = QSize(imgWidth, singleMaskHeight)
            direction = 0
        elif maskRatio <= imgRatio:          #e.g. imgRatio = 2200.0/1160 = 1896, maskRatio = 1.85
            singleMaskWidth = (imgWidth - imgHeight * maskRatio) / 2
            maskSize = QSize(singleMaskWidth, imgHeight)
            direction = 1

#        print 'maskSize:', maskSize
        maskPixmap = QPixmap(maskSize)
        maskPixmap.fill(QColor(0, 0, 0))
        alphaPixmap = QPixmap(maskSize)
        alphaPixmap.fill(QColor(alpha, alpha, alpha, alpha))
        maskPixmap.setAlphaChannel(alphaPixmap)

        return direction, maskPixmap
        
    @staticmethod
    def getLogo(logoFile, scaleFactor):
        """ """
        logoImg = QPixmap(logoFile)
        logoSize = logoImg.size()
        logoImg = logoImg.scaledToHeight(logoSize.height() * scaleFactor, Qt.SmoothTransformation)
    
        return logoImg

    @staticmethod
    def drawOneImg(maskPixmap, direction, logoImg, \
                                whiteColor, whiteFont, orangeColor, orangeFont, \
                                status, date, timecode, artist, filename, frame, \
                                scaleFactor, finalImgSize, imgSize, output, originImg, frameDAll, secImg = ''):
        """ """
        maskSize = maskPixmap.size()
        charSize = whiteFont.pixelSize() * 0.5
        blackBG = QPixmap(finalImgSize)
        blackBG.fill(QColor(1, 0, 0))
        bg = QPixmap(originImg)
        saveImg = QImage(finalImgSize, QImage.Format_ARGB32_Premultiplied)
        
        painter = QPainter()
        painter.begin(saveImg)
        painter.drawPixmap(0, 0, blackBG)
        
        #calcuate x and y
        x, y= FnImgHandle.bgStartPos(imgSize)
        print (imgSize)
        #draw the original image
        if not Config.doubleInput:
            bg = bg.scaled(imgSize, transformMode = Qt.SmoothTransformation)
            painter.drawPixmap(x, y, bg)
            if Config.drawWatermark:
                #draw masks
                opcLayerPixmap = FnDrawMask.drawMask(status, date, timecode, frame, filename, artist, 
                                                                                whiteFont,  whiteColor, orangeFont, orangeColor, 
                                                                                logoImg, maskPixmap, maskSize, 0, 0, saveImg, direction, scaleFactor, charSize, frameDAll)
                painter.drawPixmap(0, 0, opcLayerPixmap)
          
        else:
            bg = bg.scaled( imgSize.width()/2, imgSize.height(), transformMode = Qt.SmoothTransformation)
            
            secBg = QPixmap(secImg)
            secBg = secBg.scaled( imgSize.width()/2, imgSize.height(), transformMode = Qt.SmoothTransformation)

            painter.drawPixmap(x, y, bg)
            painter.drawPixmap(saveImg.size().width()/2, y, secBg)
            
            if Config.drawWatermark:
                opcLayerPixmap = FnDrawMask.drawMask(status, date, timecode, frame, filename, artist, 
                                                                                whiteFont,  whiteColor, orangeFont, orangeColor, 
                                                                                logoImg, maskPixmap, maskSize, 0, 0, saveImg, direction, scaleFactor, charSize)
                                                                    
                painter.drawPixmap(0, 0, opcLayerPixmap)
                painter.drawPixmap(saveImg.size().width()/2, 0, opcLayerPixmap)
            
        #save file with watermark
        painter.end()
        saveImg.save(QString(output), 'jpg', quality = 100)


        
    @staticmethod
    def drawMask(status, date, timecode, frame, filename, artist, whiteFont,  whiteColor, orangeFont, orangeColor, 
                            logoImg, maskPixmap, maskSize, maskX, maskY, saveImg, direction, scaleFactor, charSize, frameDAll):
        """ """
        prjCode = filename.split('_')[0]
        
        opcLayerPixmap = QPixmap(saveImg.size())
        opcLayerPixmap.fill(QColor(0, 0, 0))
        alphaPixmap = QPixmap(saveImg.size())
        alphaPixmap.fill(QColor(0, 0, 0, 0))
        opcLayerPixmap.setAlphaChannel(alphaPixmap)
        
        maskPainter = QPainter()
        maskPainter.begin(opcLayerPixmap)
        maskPainter.drawPixmap(maskX, maskY, maskPixmap)
        if direction == 0:              #up-bottom
            bottomH = saveImg.size().height() - maskSize.height() 
            maskPainter.drawPixmap(0, bottomH, maskPixmap)
        elif direction == 1:            #left-right
            rightW = saveImg.size().width() - maskSize.width()
            maskPainter.drawPixmap(rightW, 0, maskPixmap)
        
        #left-up corner: logo
        #logoX = 0 + Config.wmLeftDist * scaleFactor
        #if direction == 0:
        #    logoY = maskSize.height() - logoImg.size().height() - Config.wmBorderDist
        #elif direction == 1:
        #    logoY = 0
        #maskPainter.drawPixmap(logoX, logoY, logoImg)
        
        #left-up: prjCode
        if direction == 0:
            upY = maskSize.height() - 1 * charSize - Config.wmBorderDist * scaleFactor
        elif direction == 1:
            upY = logoImg.size().height() - Config.wmBorderDist * scaleFactor
        prjCodeX = 80
        maskPainter.setFont(whiteFont)
        maskPainter.setPen(whiteColor)
        maskPainter.drawText(prjCodeX, upY, prjCode)
        
        #middle-up: status
        lenStat = len(status) + len('STATUS: ')
        statusLX = (saveImg.size().width() - lenStat * charSize) / 2
        maskPainter.setFont(whiteFont)
        maskPainter.setPen(whiteColor)
        maskPainter.drawText(statusLX, upY, 'STATUS: ')
        
        statusCX = statusLX + len('STATUS: ') * charSize + 5
        maskPainter.setFont(orangeFont)
        maskPainter.setPen(orangeColor)
        maskPainter.drawText(statusCX, upY, status)
            
        #right-up corner: date
        lenDate = len(date)
        dateX = saveImg.size().width() - lenDate * charSize - 4*Config.wmRightDist * scaleFactor
        maskPainter.setFont(whiteFont)
        maskPainter.setPen(whiteColor)
        maskPainter.drawText(dateX, upY, date)
        
        #left-bottom corner: timecode
        if direction == 0:
            bottomY = saveImg.size().height() - maskSize.height() + Config.wmBorderDist * scaleFactor + charSize * 2.5
        else:
            bottomY = saveImg.size().height() - logoImg.size().height() + Config.wmBorderDist * scaleFactor + charSize * 2.5
        lenTimeCode = len(timecode) + len('TC: ')
        timecodeLX = 80
        maskPainter.setFont(whiteFont)
        maskPainter.setPen(whiteColor)
        maskPainter.drawText(timecodeLX, bottomY, 'TC: ')
        
        timecodeCX = timecodeLX + len('TC: ') * charSize +20 * scaleFactor
        maskPainter.setFont(orangeFont)
        maskPainter.setPen(orangeColor)
        maskPainter.drawText(timecodeCX, bottomY, timecode)
        
        #right-bottom corner: frame
        lenFrame = len(frameDAll) 
        frameLX = saveImg.size().width() - lenFrame * charSize - 4*Config.wmRightDist * scaleFactor
       
        frameCX = frameLX 
        maskPainter.setFont(orangeFont)
        maskPainter.setPen(orangeColor)
        maskPainter.drawText(frameCX, bottomY, frameDAll)
        
        #right-bottom: filename
        lenFilename = len(filename)
        filenameX = frameLX - lenFilename * charSize - 50 * scaleFactor
        maskPainter.setFont(whiteFont)
        maskPainter.setPen(whiteColor)
        maskPainter.drawText(filenameX, bottomY, filename)
        
        #middle-bottom: artist
        lenArtist = len(artist) + len('ARTIST: ')
        artistLX = statusLX - 20 * scaleFactor
        maskPainter.setFont(whiteFont)
        maskPainter.setPen(whiteColor)
        maskPainter.drawText (artistLX, bottomY, 'ARTIST: ')
        
        artistCX = artistLX + len('ARTIST: ') * charSize
        maskPainter.setFont(orangeFont)
        maskPainter.setPen(orangeColor)
        maskPainter.drawText(artistCX, bottomY, artist)
        
        maskPainter.end()
        
        if Config.doubleInput:
            opcLayerPixmap = opcLayerPixmap.scaled( saveImg.size().width()/2, saveImg.size().height(), transformMode = Qt.SmoothTransformation)
        
        return opcLayerPixmap
        

    @staticmethod
    def drawSequence(parent, alpha, finalImgSize, imgSize, scaleFactor, maskRatio, slateInfo, outputPath, 
                                    originPath, files, secPath='', secFiles = [], dpxFiles = [], dpxPath = ''):
        """ """
        running = True
        filename = files[0].split('.')[0]
        direction, maskPixmap = FnDrawMask.getMask(finalImgSize, alpha, maskRatio)
        logoImg = FnDrawMask.getLogo(QString(Config.logo), 1.0 * scaleFactor)
        whiteColor = Config.white
        orangeColor = Config.orange
        whiteFont = QFont('Arial')
        whiteFont.setPixelSize(28 * scaleFactor)
#        whiteFont.setPixelSize(28)
        orangeFont = whiteFont
        
        progress = QProgressDialog('Converting...', ' Cancel ', 0, len(files), None)
        progress.setFixedSize(QSize(400, 100))
        progress.setWindowModality(Qt.WindowModal)
        progress.setWindowFlags(Qt.WindowStaysOnTopHint)
        progress.show()
        #print files
        for index in range(len(files)):
            file = files[index]
            try:
                artist = file.split('_')[2]
            except:
                artist = ''
            namesplit = file.split('.')
            frame = namesplit[1]
            end = int(files[-1].split('.')[1])
            frameNo = str(frame)
            frameDAll =(frameNo[1:4]) +'/'+str(end)
            ext = namesplit[-1]
            outputname = namesplit[0] + '.' + frame + '.jpg'
            outputfile = os.path.join(outputPath, outputname)
#            print 'outputfile:', outputfile

            fstfile = os.path.join(originPath, file)
            try:
                dpxfile = os.path.join(dpxPath, dpxFiles[index])
                timecode = FnImgHandle.readDPXTimecode(dpxfile)
            except:
                timecode = ''
            progress.setLabelText(QString(u'正在转换 %d / %d ' % (index, len(files))))
            progress.setValue(index)
            progress.update()
            if progress.wasCanceled():
                running = False
                break
                
            if not Config.doubleInput:
                FnDrawMask.drawOneImg(maskPixmap, direction, \
                                                        logoImg, \
                                                        whiteColor, whiteFont, orangeColor, orangeFont, \
                                                        slateInfo.status, slateInfo.date, timecode, artist, slateInfo.shot, frame, \
                                                        scaleFactor, finalImgSize, imgSize, outputfile, fstfile, frameDAll)
            else:
                secFullfile = os.path.join(secPath, secFiles[index])
                FnDrawMask.drawOneImg(maskPixmap, direction, \
                                                        logoImg,  \
                                                        whiteColor, whiteFont, orangeColor, orangeFont, \
                                                        slateInfo.status, slateInfo.date, timecode, artist, slateInfo.shot, frame, \
                                                        scaleFactor, finalImgSize, imgSize, outputfile, fstfile, secFullfile, frameDAll)
        return running
        
    @staticmethod
    def usefulFiles(shotname, originPath):
        files = os.listdir(originPath)
        files.sort()
        rmList = []
        for file in files:
            fullfile = os.path.join(originPath, file)
            if os.path.isdir(fullfile):
                rmList.append(file)
            elif shotname not in file:
                rmList.append(file)
                
        for rm in rmList:
            files.remove(rm)
        return files
        
    @staticmethod
    def saveSequence(parent, alpha, maskRatio, finalImgSize, imgSize, slateInfo, outputPath, shotname, originPath, secShotname = '', secPath = '', dpxname = '', dpxPath = '' ):
        """ """
        running = True
        files = FnDrawMask.usefulFiles(shotname, originPath)
        secFiles = []
        if secPath != '':
            secFiles = FnDrawMask.usefulFiles(secShotname, secPath)
            
        dpxFiles = []
        if dpxPath != '':
            dpxFiles = FnDrawMask.usefulFiles(dpxname, dpxPath)

        scaleFactorH = finalImgSize.height() * 1.0 / Config.basicSlateSize.height()
        scaleFactorW = finalImgSize.width() * 1.0 / Config.basicSlateSize.width()
        if scaleFactorH > scaleFactorW:
            scaleFactor = scaleFactorW
        else:
            scaleFactor = scaleFactorH
            
        try:
            Config.FINALTMPFOLDER = FnImgHandle.createTmpFolder(outputPath)
            running = FnDrawMask.drawSequence(parent, alpha, finalImgSize, imgSize, scaleFactor, maskRatio, slateInfo, \
                                                        Config.FINALTMPFOLDER, originPath, files, secPath, secFiles, dpxFiles, dpxPath)
        except OSError, e:
            running = False
            print e
            QMessageBox .critical(None, 'ERROR', u' FnDrawMask::saveSequence(): %s ' % str(e).decode('utf-8'), QString('OK'))
            
        return running
        

        
        
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    
    basicImgSize = Config.basicSlateSize

    imgSize = QSize(2200, 1160)
    scaleFactor = imgSize.height() * 1.0 / basicImgSize.height()
    direction, maskPixmap = FnDrawMask.getMask(imgSize, 128, 2.35)
    logoImg = FnDrawMask.getLogo(QString(Config.logo), 1.0 * scaleFactor)
    whiteColor = Config.white
    orangeColor = Config.orange
    whiteFont = QFont('Arial')
    whiteFont.setPixelSize(28 * scaleFactor)
    orangeFont = whiteFont

    Config.doubleInput = True
    FnDrawMask.drawOneImg(maskPixmap, direction, logoImg, maskPixmap.size(), \
                                            whiteColor, whiteFont, orangeColor, orangeFont, \
                                            'Precomp', '05/09/2013 17:00', '23:05:47:15', 'wangjb', 'drj_cmp_wangjb_final_v001_15', '124', \
                                            1.0, '/JGHome/xiangquan/oiio_test/wm.0101.jpg', \
                                            '/JGHome/xiangquan/oiio_test/drj03706_cmp_wangjb_final_v001_15/drj03706_cmp_wangjb_final_v001_15.0101.jpg', \
                                            '/JGHome/xiangquan/oiio_test/drj03706_cmp_wangjb_final_v001_15/drj03706_cmp_wangjb_final_v001_15.0101.jpg')

