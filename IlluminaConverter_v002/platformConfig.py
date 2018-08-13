#!/usr/bin/env python2.6
#-*- coding: utf-8 -*-

# Filename: platformConfig.py
# Author: XueFeng, Xiangquan
# Created: 2012/07/02/
# Latest Modified: 2013/04/24/
# Platform: Ubuntu10.04
# Copyright: Illumina ltd, PTD department, 2012

import os
import platform


class PlatformConfig(object):
    """This Class Config Platform. Windows & Linux ."""
    @staticmethod
    def softwarePath():
        """mencoder & mp4creator Path in Windows & Linux ."""
        if platform.system() == "Windows":
            mencoderPath = '//192.168.100.100/Public/Ptd/Softwares/mencoder/mencoder'
            mp4creatorPath = '//192.168.100.100/Public/Ptd/Softwares/mp4creator/mp4creator'
        elif platform.system() == 'Linux':
            mencoderPath = 'mencoder'
            mp4creatorPath = 'mp4creator'
        return mencoderPath, mp4creatorPath
    
    @staticmethod
    def tempFilePath():
        """Temp File Path in Windows & Linux ."""
        if platform.system() == 'Windows':
            tmpOutPath1 = 'D:/tmp1'
            tmpOutPath2 = 'D:/tmp2.h264'
        elif platform.system() == 'Linux':
            tmpOutPath1 = os.environ['HOME'] + '/tmp1'
            tmpOutPath2 = os.environ['HOME'] + '/tmp2.h264'
        return tmpOutPath1, tmpOutPath2
    
    @staticmethod
    def changeDirPath():
        """Project Directory Path in Windows & Linux ."""
        if platform.system() == 'Windows':
            directory = "D:/"
        elif platform.system() == 'Linux':
            directory = os.environ['HOME']
        return directory
    
    @staticmethod
    def divxFilePath():
        """Temp File divx2pass.log Path in Windows & Linux ."""
        if platform.system() == 'Windows':
            divx1 = 'D:/divx2pass.log'
            divx2 = 'D:/divx2pass.log.mbtree'
        elif platform.system() == 'Linux':
            divx1 = os.environ['HOME'] + '/divx2pass.log'
            divx2 = os.environ['HOME'] + '/divx2pass.log.mbtree'
        return divx1, divx2
    @staticmethod
    def createMovCommand(cmd_1, cmd_2, cmd_3):
        """os.system(cmd) in Linuxs os.popen(cmd) in Windows"""
        os.popen(cmd_1)
        os.popen(cmd_2)
        os.popen(cmd_3)
        
#        if platform.system() == 'Windows':
#            os.popen(cmd_1)
#            os.popen(cmd_2)
#            os.popen(cmd_3)
#        elif platform.system() == 'Linux':
#            os.system(cmd_1)
#            os.system(cmd_2)
#            os.system(cmd_3)
