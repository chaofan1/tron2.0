#!/usr/bin/env python2.6
#-*- coding: utf-8 -*-

# Filename: dirAnalyse.py
# Author: Xiangquan, XueFeng
# Created: 2012/07/02/ 13:00
# Latest Modified: 2012/07/04/ 13:00
# Platform: Windows7
# Copyright: Illumina ltd, PTD department, 2012

import os
import os.path
import re

import PythonMagick
from PyQt4.QtCore import QSize
from fnImgHandle import FnImgHandle
from config import Config

class DirAnalyse(object):
    def __init__(self, inputpath, dpxpath = ''):
        """ Constructor"""
        self.fullpath = inputpath
        #print inputpath
        self.path = os.path.dirname(self.fullpath)
        self.dpxpath = dpxpath
        self.files = self.filterFiles(self.path)
        self.titlename = ''
        self.version = ''
        self.shotname = ''
        self.format = ''
        self.duration = ''
        self.resolution = ''
        self.timecode = self.getDpxTimecode(self.dpxpath)
        if self.files != []:
            self.titlename, self.version, self.shotname, self.format = self.getPrefixInfo(self.files[0])
            self.duration = self.getDuration(self.files)
            self.resolution = self.getResolution(self.path, self.files[0])
        
#        print self.titlename
#        print self.version
#        print self.shotname
#        print self.duration
#        print self.resolution
        #print self.format
#        
    def filterFiles(self, path):
        """ """
        filename = os.path.basename(self.fullpath)     #the "Shot" info. of a slate
        ext = os.path.splitext(filename)[1]
        prefix = filename.split('.')[0]
#        print 'filename:', filename, 'ext:', ext, 'prefix:', prefix
        
        files = []
        if os.path.exists(path):
            allfiles = os.listdir(path)
            for file in allfiles:
                filePrefix = file.split('.')[0]
                fileExt = '.' +  file.split('.')[-1]
#                print 'filePrefix:', filePrefix,  'fileExt:', fileExt
                if prefix == filePrefix and ext == fileExt:
                    files.append(file)
            files.sort()
        return files
        
    def getDuration(self, files):
        duration = ''
        try:
            start = int(files[0].split('.')[1])
            end = int(files[-1].split('.')[1])
            duration = str(start) + ' - ' + str(end)
        except ValueError, e:
            print e
        except IndexError, e:
            print e
            
        return duration
        
    def getIntResolution(self, path, file):
        filepath = os.path.join(path, file)
        imgReader = PythonMagick.Image(str(filepath))
        resolution = QSize(imgReader.size().width(), imgReader.size().height()) * Config.resFactor
        #print resolution
        return resolution
        
    def getResolution(self, path, file):
        resolution = self.getIntResolution(path, file)
        if Config.resIndex != Config.HD:
            unicodeRes = unicode(str(resolution.width()) + 'x' + str(resolution.height())) 
        else:
            unicodeRes = unicode(u'1920x1080')

        return unicodeRes
        
    def getPrefixInfo(self, file):
        shotname = file.split('.')[0]
        format = file.split('.')[-1]
        splits = shotname.split('_')
        titlename = splits[0]               #tgr00608
#        titlename = titlename[002:]
        regr = re.compile('v[0-9]{002}_[0-9]{2}')
        version = ''
        m = re.search(regr, shotname)
        if m is not None:
            version = m.group()
            
        return titlename, version, shotname, format
        
    def getDpxTimecode(self, dpxpath):
        """ """
        timecode = FnImgHandle.readDPXTimecode(dpxpath.__str__())
        return timecode
        
if __name__ == '__main__':
#    input = '/JGHome/xiangquan/oiio_test/tgr/dfasdgtadg.%04d.jpeg'
    input = '/Users/liangcy/Desktop/IMG_20151201_102105.jpg'
    dirAnalyse = DirAnalyse(input)
        
        
        
