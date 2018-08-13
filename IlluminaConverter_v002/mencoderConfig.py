#!/usr/bin/env python2.6
#-*- coding: utf-8 -*-

# Filename: mencoderConfig.py
# Author: XueFeng
# Created: 2012/07/02/ 13:00
# Latest Modified: 2013/01/08/ 13:00
# Platform: Ubuntu10.04
# Copyright: Illumina ltd, PTD department, 2012

import os

from PIL import Image
from PIL import TiffImagePlugin
from PIL import TgaImagePlugin


class MencoderConfig(object):
    """Config of Mencorder to Convert Mov ."""
    @staticmethod
    def resltFunc(selFile, selReslt):
        """Return Image File Width and Height ."""
        selFile = selFile
        if selReslt == 'Original':
            im = Image.open(selFile)
            width = im.size[0]
            height = im.size[1]
        elif selReslt == 'Half':
            im = Image.open(selFile)
            width = int(im.size[0] / 2)
            height = int(im.size[1] / 2)
        # !v02  Add Dailies Function 
        elif selReslt == 'Dailies':
            im = Image.open(selFile)
            if im.size[0]>1920:
                width = 1920
                height = int(1920.0/im.size[0]*im.size[1])
                print width,height
            else:
                im = Image.open(selFile)
                width = im.size[0]
                height = im.size[1]
        #-----------------------------end
        else:
            selReslt = selReslt.split('*')
            width = selReslt[0]
            height = selReslt[1]
        return width, height
    
    @staticmethod
    def qualityFunc(selQuality):
        """Return bitrate and qp According As Quality ."""
        quality = selQuality
        bitrate = 900
        qp = 23        # qp is parameter of mencorder convert command .
        if quality == 'High':
            bitrate = 900
            qp = 23
        elif quality == 'Medium':
            bitrate = 900
            qp = 26
        elif quality == 'Low':
            bitrate = 900
            qp = 29
        elif quality == 'Very High':
            bitrate = 1200
            qp = 20
        return bitrate, qp
    
    @staticmethod
    def textPath(outPath, filePre):
        """Save Text File Path ."""
        textPath = outPath + os.sep + filePre + '.txt'
        return textPath
    
    @staticmethod
    def saveText(outPath, convertPath, filePre, convertList):
        """Save Mencorder convert Mov Text .
        Text Contain Images Path List ."""
        textPath = MencoderConfig.textPath(outPath, filePre)
        textFile = open(textPath, 'w+')
        for i in convertList:
            textFile.write(convertPath + os.sep + i + '\n')
            textFile.flush()
        textFile.close()
