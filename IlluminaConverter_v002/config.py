#!/usr/bin/env python2.6
#-*- coding: utf-8 -*-

# Filename: config.py
# Author:  Xiangquan
# Created: 2013/05/06/
# Latest Modified: 2013/05/06/
# Platform: Ubuntu10.04
# Copyright: Illumina ltd, PTD department, 2012

import os
import os.path
import sys
import platform
import getpass

from PyQt4.QtGui import QColor
from PyQt4.QtCore import QSize, QString

def getConfigInfo(line):
    infoStr = line
    infoStr = infoStr.replace('\n', '')
    infoStr = infoStr.split('=')[1]
    infoList = infoStr.split(', ')
    
    return infoList
    
def getUser():
    username = getpass.getuser()
    return username

class Config(object):
    """ """
    repaint = 0
    
    winStart = QString('Tron_Converter')
    winError = QString('Terminated')
    winRun = QString('Running...')
    winDone = QString('Finished.')
    
    if platform.system() == 'Linux':
        slateBG = '/Public/System/Tron/IlluminaConverter_v002/ubuntu/doc/design/slateBG_v1.png'
        logoBG = '/Public/System/Tron/IlluminaConverter_v002/ubuntu/icon/logo.png'
        realSlate = '/Public/System/Tron/IlluminaConverter_v002/ubuntu/doc/design/slateBG_v2.png'
        logo = '/Public/System/Tron/IlluminaConverter_v002/ubuntu/doc/design/logo_20.png'
        
        xIcon = '/Public/System/Tron/IlluminaConverter_v002/ubuntu/icon/x.png'
        resolutionIcon = '/Public/System/Tron/IlluminaConverter_v002/ubuntu/icon/resolutionIcon.png'
        frameIcon = '/Public/System/Tron/IlluminaConverter_v002/ubuntu/icon/frameIcon.png'
        outputIcon = '/Public/System/Tron/IlluminaConverter_v002/ubuntu/icon/outputIcon.png'

        textFont = 'AR PL UKai CN'
        
        defaultDir = '/All'
        fp = open('/Public/System/Tron/IlluminaConverter_v002/ubuntu/config/config.txt')
        
    elif platform.system() == 'Windows':
        slateBG = '//192.168.100.99/Public/System/Tron/IlluminaConverter_v002/doc/design/slateBG_v1.png'
        logoBG = '//192.168.100.99/Public/System/Tron/IlluminaConverter_v002/icon/logo.png'
        realSlate = '//192.168.100.99/Public/System/Tron/IlluminaConverter_v002/doc/design/slateBG_v2.png'
        logo = '//192.168.100.99/Public/System/Tron/IlluminaConverter_v002/doc/design/logo_20.png'
        
        xIcon = '//192.168.100.99/Public/System/Tron/IlluminaConverter_v002/icon/x.png'
        resolutionIcon = '//192.168.100.99/Public/System/Tron/IlluminaConverter_v002/icon/HD.png'
        frameIcon = '//192.168.100.99/Public/System/Tron/IlluminaConverter_v002/icon/FPS.png'
        maskIcon = '//192.168.100.99/Public/System/Tron/IlluminaConverter_v002/icon/MK.png'
        videoIcon = '//192.168.100.99/Public/System/Tron/IlluminaConverter_v002/icon/VC.png'
        outputIcon = '//192.168.100.99/Public/System/Tron/IlluminaConverter_v002/icon/folder.png'
        
        textFont = u'Adobe 楷体 Std R'

        defaultDir = '//192.168.100.99/Public/System/Tron/IlluminaConverter_v002/'
        fp = open('//192.168.100.99/Public/System/Tron/IlluminaConverter_v002/config/config.txt','rb')

    elif platform.system() == "Darwin" :

        slateBG = '/Users/liangcy/Desktop/TronInter/tronPipelineScript/IlluminaConverter_v002/doc/design/slateBG_v1.png'
        logoBG = '/Users/liangcy/Desktop/TronInter/tronPipelineScript/IlluminaConverter_v002/icon/logo.png'
        realSlate = '/Users/liangcy/Desktop/TronInter/tronPipelineScript/IlluminaConverter_v002/doc/design/slateBG_v2.png'
        logo = '/Users/liangcy/Desktop/TronInter/tronPipelineScript/IlluminaConverter_v002/doc/design/logo_20.png'

        xIcon = '/Users/liangcy/Desktop/TronInter/tronPipelineScript/IlluminaConverter_v002/icon/x.png'
        resolutionIcon = '/Users/liangcy/Desktop/TronInter/tronPipelineScript/IlluminaConverter_v002/icon/HD.png'
        frameIcon = '/Users/liangcy/Desktop/TronInter/tronPipelineScript/IlluminaConverter_v002/icon/FPS.png'
        maskIcon = '/Users/liangcy/Desktop/TronInter/tronPipelineScript/IlluminaConverter_v002/icon/MK.png'
        videoIcon = '/Users/liangcy/Desktop/TronInter/tronPipelineScript/IlluminaConverter_v002/icon/VC.png'
        outputIcon = '/Users/liangcy/Desktop/TronInter/tronPipelineScript/IlluminaConverter_v002/icon/folder.png'

        textFont = u'Adobe 楷体 Std R'

        defaultDir = '/Volumes/Public/System/Tron/IlluminaConverter_v002/'
        fp = open('/Users/liangcy/Desktop/TronInter/tronPipelineScript/IlluminaConverter_v002/config/config.txt', 'rb')
    filters = fp.readlines()
    status = getConfigInfo(filters[0])
    lut = getConfigInfo(filters[1])
    maskRatio = getConfigInfo(filters[2])

    orange = QColor(247, 148, 30)
    white = QColor(255,  255,  255)
    bgGray = QColor(51, 51, 51)
    textGray = QColor(156, 156, 156)
    
    originRatio = 16.0 / 9.0        # assume originRadio = 16 / 9 = 1.777
    basicSlateSize = QSize(1920,  1080)
    basicTbSize = QSize(416, 234)
    
    scaleFactor = 0.603125
    titleFontSize = 30
    verFontSize = 20
    contentFontSize = 20
    textEditSize = 24
    slateInfoSize = 28
    
    titleDist = 90
    titleToVer = 45
    optionToVer = 20                #original distance from "VFX Code" to the white version code
    optionToLeft = 190              #original distance from "VFX Code" to the left border of a HD slate 
    optionToRight = 200
    optiontoTextEdit = 36
    optionSpacing = 8
    
    descriptionList = []
    feedbackList = []
    
    resFactor = 1.0
    resIndex = 0
    HD = 0
    Original = 1
    Half = 2
    
    HDFactor = 1.777
    halfOpc = 125           #mask half opacity
    fullOpc = 255            #mask full opacity
    noOpc = 0                 #no mask
    
    wmLeftDist = 20
    wmBorderDist = 5
    wmRightDist = 20
    
    doubleInput = False
    drawSlate = 2
    drawWatermark = 2
    
    OPENEXTS = '*.jpg *.jpeg \n*.png \n*.tiff \n*.tga *.dpx\n*.*'         #the file's extension
    TOJPG = ['tga', '.tga', 'dpx', '.dpx', 'exr', '.exr']

    TMPFOLDER = 'tmp_' + getUser()  + '0'
    FINALTMPFOLDER = ''
    SPECIMGFOLDER0 = ''             #if has double inputs, this is the first input
    SPECIMGFOLDER = ''
    
    runStatus = True

#if __name__ == '__main__':
#    print Config.TMPFOLDER
