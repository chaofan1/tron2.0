#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

# Filename: fnImgHandle.py
# Author:  Xiangquan
# Created: 2013/05/09/
# Latest Modified: 2013/05/09/
# Platform: Ubuntu10.04
# Copyright: Illumina ltd, PTD department, 2012

import os
import array
import platform

from PIL import Image
from PIL import ImageEnhance
import PythonMagick
import OpenEXR
import Imath

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from config import Config


class FnImgHandle(object):
    def __init__(self):
        """ Constructor"""
        pass

    @staticmethod
    def reduce_opacity(m, opacity):
        """Returns an image with reduced opacity."""
        assert opacity >= 0 and opacity <= 1
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        else:
            im = im.copy()
        alpha = im.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        im.putalpha(alpha)

        return im

    @staticmethod
    def opacityImg(imgName, opacity, saveFilename):
        """ imgName = /JGHome/xiangquan/oiio_test/logo.png"""
        path = os.path.dirname(imgName)
        logoim = Image.open(imgName)
        newlogoim = FnImgHandle.reduce_opacity(logoim, opacity)
        newlogoName = os.path.join(path, saveFilename)
        newlogoim.save(newlogoName, quality=100)

    @staticmethod
    def readDPXTimecode(dpxImgFile):
        """ dpxImgFile: the full path of a dpx file"""
        timecode = ''
        if dpxImgFile is not None and os.path.exists(dpxImgFile):
            image = PythonMagick.Image(str(dpxImgFile))
            print image
            timecode = image.attribute('dpx:television.time.code')

        return timecode

    @staticmethod
    def createTmpFolder(outputPath):
        """ """
        tmpDir = os.path.join(outputPath, Config.TMPFOLDER)
        i = 0
        while os.path.exists(tmpDir):
            i += 1
            tmpDir = tmpDir[:-1] + str(i)

        tmpDir += '/'
        os.mkdir(tmpDir)
        return tmpDir

    @staticmethod
    def exr2jpg(exrfile, jpgfile):
        file = OpenEXR.InputFile(exrfile)
        pt = Imath.PixelType(Imath.PixelType.FLOAT)
        dw = file.header()['dataWindow']
        size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)

        redStr = file.channel('R', pt)
        greenStr = file.channel('G', pt)
        blueStr = file.channel('B', pt)

        red = array.array('f', redStr)  # 'f' : float
        green = array.array('f', greenStr)
        blue = array.array('f', blueStr)

        def EncodeToSRGB(v):
            if v == 0.0:
                return v
            elif v <= 0.0031308:
                return v * 3294.6  # (v * 12.92) * 255.0
            else:
                return 265.025 * (v ** 0.42) - 14.025  # (1.055 * (v ** (1.0 / 2.4)) - 0.055) * 255.0

        for i in range(len(red)):
            red[i] = EncodeToSRGB(red[i])

        for i in range(len(green)):
            green[i] = EncodeToSRGB(green[i])

        for i in range(len(blue)):
            blue[i] = EncodeToSRGB(blue[i])

        rgbf = [Image.fromstring('F', size, red.tostring())]
        rgbf.append(Image.fromstring('F', size, green.tostring()))
        rgbf.append(Image.fromstring('F', size, blue.tostring()))

        rgb8 = [elem.convert('L') for elem in rgbf]

        Image.merge('RGB', rgb8).save(jpgfile, quality=100)

    @staticmethod
    def convertImgToJpg(specFile, jpgFile):
        if os.path.splitext(specFile)[1] == '.exr':
            FnImgHandle.exr2jpg(specFile, jpgFile)
        else:
            image = PythonMagick.Image(str(specFile))
            image.write(str(jpgFile))

    @staticmethod
    def convertImgsToJpgs(files, specImgDir, outputPath):
        """ save these jpgs to outputPath/tmp"""
        hasSpecImg = False
        outputTmp = FnImgHandle.createTmpFolder(outputPath)

        progress = QProgressDialog('Handling...', ' Cancel ', 0, len(files), None)
        progress.setFixedSize(QSize(400, 100))
        progress.setWindowModality(Qt.WindowModal)
        progress.show()
        for file in files:
            index = files.index(file)
            progress.setLabelText(QString(u'正在处理图像 %d / %d ' % (index, len(files))))
            progress.setValue(index)
            progress.update()

            if progress.wasCanceled():
                break

            splits = os.path.splitext(file)
            if splits[1] in Config.TOJPG:
                hasSpecImg = True
                tgaFile = os.path.join(specImgDir, file)
                newname = splits[0] + '.jpg'
                jpgFile = os.path.join(outputTmp, newname)
                FnImgHandle.convertImgToJpg(tgaFile, jpgFile)
        if hasSpecImg:
            #            Config.SPECIMGFOLDER = outputTmp
            return outputTmp
        else:
            return specImgDir

    @staticmethod
    def scaleImage(image, imgSize):
        """image: QImage or QPixmap; imgSize: the size of the sequence imgs"""
        tbSize = image.size()
        originRadio = imgSize.width() * 1.0 / imgSize.height()  # assume originRadio = 16 / 9 = 1.777
        radio = tbSize.width() * 1.0 / tbSize.height()

        startX = 0
        startY = 0
        if radio < originRadio:  # assume radio = 4 / 002 = 1.333
            image = image.scaledToHeight(imgSize.height(), Qt.SmoothTransformation)
            newTbW = image.size().width()
            startX = (imgSize.width() - newTbW) / 2
        else:
            image = image.scaledToWidth(imgSize.width(), Qt.SmoothTransformation)
            newTbH = image.size().height()
            startY = (imgSize.height() - newTbH) / 2

        return startX, startY, image

    @staticmethod
    def HDSize(imgSize):
        """calcuate w and h """
        originRatio = imgSize.width() * 1.0 / imgSize.height()
        #        print 'origin Ratio:', originRatio
        if originRatio < Config.HDFactor:
            height = 1080
            width = height * originRatio
        elif originRatio > Config.HDFactor:
            width = 1920
            height = width / originRatio
        else:
            width = 1920
            height = 1080

        return width, height

    @staticmethod
    def bgStartPos(imgSize):
        """ """
        if Config.resIndex == Config.HD:  # HD
            imgRatio = imgSize.width() * 1.0 / imgSize.height()
            if imgRatio < Config.HDFactor:
                x = (1920 - imgSize.width()) / 2
                y = 0
            elif imgRatio > Config.HDFactor:
                x = 0
                y = (1080 - imgSize.height()) / 2
            else:
                x = 0
                y = 0
        else:  # Original and Half
            x = 0
            y = 0
        return x, y


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    img = QImage('D:/testJpeg/fst_rig_wangcy_dementor_master/fst_rig_wangcy_dementor_master.0100.jpg')
    FnImgHandle.scaleImage(img, QSize(160, 90))
    timecode = FnImgHandle.readDPXTimecode(
        'D:/testJpeg/fst_rig_wangcy_dementor_master/fst_rig_wangcy_dementor_master.0100.jpg')
    print timecode
    sys.exit(app.exec_())
