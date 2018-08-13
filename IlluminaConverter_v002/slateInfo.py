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

from PIL import Image        #, ImageEnhance

class SlateInfo(object):
    def __init__(self, vfxcode = '', shot = '', duration = '', handles = '', timecode = '', status = '', date = '', \
                        lut = '', maskRatio = '', resolution = '', format = '', description = [], feedback = []):
        """ Constructor """
        self.vfxcode = vfxcode
        self.shot = shot
        self.duration = duration
        self.handles = handles
        self.timecode = timecode
        self.status = status
        self.date = date
        self.lut = lut
        self.maskRatio = maskRatio
        self.resolution = resolution
        self.format = format
        self.description = description
        self.feedback = feedback
        self.dirAnalyse = ''
        
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    input = 'D:/testJpeg/fst_rig_wangcy_dementor_master/fst_rig_wangcy_dementor_master_04.$F4.jpg'
    dirAnalyse = DirAnalyse(input)
    
    sys.exit(app.exec_())


