#!/usr/bin/env python2.6
#-*- coding: utf-8 -*-

# Filename: convertThread.py
# Author: Xiangquan
# Created: 2013/04/24/
# Latest Modified: 2013/04/24/
# Platform: Ubuntu10.04
# Copyright: Illumina ltd, PTD department, 2012

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from mencoderConfig import MencoderConfig
from platformConfig import PlatformConfig
from dirCheck import DirCheck
import os

class ConvertThread(QThread): 
    """Core Command To Convert Mov ."""
    def __init__(self, progress, convertPathList, reslution, outPath, frame, bitrate, qp, parent=None): 
        """Initialize Parameters Which In Core Command ."""
        super(ConvertThread, self).__init__(parent)
        self.progress = progress
        self.convertPathList = convertPathList
        self.reslution = reslution
        self.outPath = outPath
        self.frame = frame
        self.bitrate = bitrate
        self.qp = qp
        
    def run(self): 
        """Core Function To Convert Mov."""
        mencoderPath, mp4creatorPath = PlatformConfig.softwarePath()
        tmpOutPath1, tmpOutPath2 = PlatformConfig.tempFilePath()
        
        for convertPath in self.convertPathList:
            convertList = []
            for i in DirCheck.allFileName(convertPath):
                convertList.append(i)
            resltFile = convertPath + os.sep + convertList[0]
            width, height = MencoderConfig.resltFunc(str(resltFile), self.reslution)
            filePre = DirCheck.filePre(convertPath)
            MencoderConfig.saveText(self.outPath, convertPath, filePre, convertList)
            textPath = MencoderConfig.textPath(self.outPath, filePre)
            finalMovPath = self.outPath + os.sep + filePre + '.mov'
            
            cmd_1 = '%s mf://@%s -mf fps=%s -nosound -ovc x264 -x264encopts '  \
            'pass=1:turbo:bitrate=300:direct=auto:subq=1:frameref=1:bframes=0:trellis=1:me=umh:keyint=12 '  \
            '-noskip -of rawvideo -vf harddup,eq=5:-5,scale=%s:%s -o %s ' % (mencoderPath, textPath, self.frame, width, height, tmpOutPath1)
            cmd_2 = '%s mf://@%s -mf fps=%s -nosound -ovc x264 -x264encopts '   \
            'pass=2:turbo:bitrate=%d:direct=auto:subq=6:frameref=15:bframes=0:trellis=1:qp=%d:me=umh:qcomp=0.9:keyint=12 '\
            '-noskip -of rawvideo -vf harddup,eq=5:-5,scale=%s:%s -o %s ' % (mencoderPath, textPath, self.frame, self.bitrate, self.qp, width, height, tmpOutPath2)
            cmd_3 = '%s -create=%s -rate=%s %s 2>&1' % (mp4creatorPath, tmpOutPath2, self.frame, finalMovPath)
            
            if os.path.exists(finalMovPath):
                os.remove(finalMovPath)
            PlatformConfig.createMovCommand(cmd_1, cmd_2, cmd_3)
            os.remove(textPath)
            os.remove(tmpOutPath1)
            os.remove(tmpOutPath2)
            os.remove(PlatformConfig.divxFilePath()[0])
            os.remove(PlatformConfig.divxFilePath()[1])
            
        self.progress.reset()
        
