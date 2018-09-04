#!/usr/bin/env python2.6
#-*- coding: utf-8 -*-

# Filename: response.py
# Author:  Xiangquan
# Created: 2013/05/10/
# Latest Modified: 2013/05/10/
# Platform: Ubuntu10.04
# Copyright: Illumina ltd, PTD department, 2012

import os
import math
import time
import shutil,sys
import platform
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Ui_Layout import Ui_Layout
from fnDrawSlate import FnDrawSlate
from fnDrawMask import FnDrawMask
from fnImgHandle import FnImgHandle
from dirAnalyse import DirAnalyse
from slateInfo import SlateInfo
from config import Config


class Response(QMainWindow, Ui_Layout):
    def __init__(self, parent = None):
        self.inOutput = QApplication.argv()
        QMainWindow.__init__(self, parent)
        self.mainWindow = QMainWindow()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setFixedSize(1170, 900)
        self.screen = QDesktopWidget().screenGeometry()
        self.size = self.geometry()
        self.move((self.screen.width() - self.size.width()) / 2, (self.screen.height() - self.size.height()) / 2)
        #self.move(450, 150)
        self.setupUi(self.mainWindow)
        self.connectSignals()
        self.show()



    def connectSignals(self):
        self.transferInfo = self.leftArea.transferInfo
        self.painter = self.leftArea.painter
        self.painter.dirAnalyse = DirAnalyse(self.transferInfo.input.textUnicode(), self.transferInfo.dpxtc.textUnicode())
        #print self.transferInfo.input.textUnicode()
        #self.painter.dirAnalyse = DirAnalyse('Input Path',self.transferInfo.dpxtc.textUnicode())
        QObject.connect(self.transferInfo.input.lineEdit, SIGNAL("textChanged(QString)"), self.updateTitlePainter)
        QObject.connect(self.transferInfo.dpxtc.lineEdit, SIGNAL("textChanged(QString)"), self.updateDpxPainter)
        QObject.connect(self.transferInfo.run, SIGNAL('released()'), self.run)
        QObject.connect(self.transferInfo.doubleInput, SIGNAL('stateChanged(int)'), self.doubleInputs)
        QObject.connect(self.transferInfo.drawSlate, SIGNAL('stateChanged(int)'), self.drawSlateOrNot)
        QObject.connect(self.transferInfo.drawWatermark, SIGNAL('stateChanged(int)'), self.drawWatermarkOrNot)
        QObject.connect(self.transferInfo.resCombo.combo, SIGNAL('currentIndexChanged(int)'), self.changeResolution)
        
    def updateTitlePainter(self, input):
        """ """
        self.painter.title = input
        self.painter.dirAnalyse = DirAnalyse(self.transferInfo.input.textUnicode(), self.transferInfo.dpxtc.textUnicode())
        Config.repaint = 0
        Config.defaultDir = QString(input)
        self.painter.repaint()
        self.painter.shot.setText(self.painter.dirAnalyse.shotname)
        self.painter.duration.setText(self.painter.dirAnalyse.duration)
        self.painter.timecode.setText(self.painter.dirAnalyse.timecode)
        self.painter.date.setText(time.strftime('%m/%d/%Y %H:00', time.localtime(time.time())) )
        self.painter.resolution.setText(self.painter.dirAnalyse.resolution)
        self.painter.format.setText(self.painter.dirAnalyse.format)
        
    def updateDpxPainter(self, dpx):
        strDpx = str(dpx)
        timecode = FnImgHandle.readDPXTimecode(strDpx)
        self.painter.timecode.setText(timecode)
        
    def doubleInputs(self, state):
        """ state == 0: No, state == 2: Yes"""
        if state == Qt.Unchecked:
            self.transferInfo.input2.setEnabled(False)
        elif state == Qt.Checked:
            self.transferInfo.input2.setEnabled(True)
            
        Config.doubleInput = state
        
    def drawSlateOrNot(self, state):
        """state == 0: No, state == 2: Yes """
        Config.drawSlate = state
#        print 'drawSlate ?', Config.drawSlate
        
    def drawWatermarkOrNot(self, state):
        """state == 0: No, state == 2: Yes """
        Config.drawWatermark = state
#        print 'drawWatermark ?', Config.drawWatermark

    def changeResolution(self, index):
        """ """
        Config.resIndex = index
        if index == Config.Original:
            Config.resFactor = 1.0
            self.painter.dirAnalyse = DirAnalyse(self.transferInfo.input.textUnicode(), self.transferInfo.dpxtc.textUnicode())
            self.painter.resolution.setText(self.painter.dirAnalyse.resolution)
        elif index == Config.Half :      #half
            Config.resFactor = 0.5
            self.painter.dirAnalyse = DirAnalyse(self.transferInfo.input.textUnicode(), self.transferInfo.dpxtc.textUnicode())
            self.painter.resolution.setText(self.painter.dirAnalyse.resolution)
        elif index == Config.HD:    #HD: 1920x1080
            Config.resFactor = 1.0
            self.painter.dirAnalyse.resolution = '1920x1080'
            self.painter.resolution.setText('1920x1080')
        
    def run(self):
        """ """
        vcodec = self.transferInfo.vcodec.textStr()
        dirAnalyse = DirAnalyse(self.transferInfo.input.textUnicode(), self.transferInfo.dpxtc.textUnicode())
        imgSize = dirAnalyse.getIntResolution(dirAnalyse.path, dirAnalyse.files[0])    #   QSize
        #print (dirAnalyse.path, dirAnalyse.files[0])
        #slate info.
        self.slateInfo = SlateInfo()
        self.slateInfo.vfxcode = self.painter.vfxcode.textUnicode()
        self.slateInfo.shot = self.painter.shot.textUnicode()
        self.slateInfo.duration = self.painter.duration.textUnicode()
        self.slateInfo.handles = self.painter.handles.textUnicode()
        self.slateInfo.timecode = self.painter.timecode.textUnicode()
        self.slateInfo.status = self.painter.status.textUnicode()
        self.slateInfo.date = self.painter.date.textUnicode()
        self.slateInfo.lut = self.painter.lut.textUnicode()
        self.slateInfo.maskRatio = self.painter.maskRatio.textUnicode()
        self.slateInfo.resolution = self.painter.resolution.textUnicode()
        self.slateInfo.format = self.painter.format.textUnicode()
        self.slateInfo.description = self.painter.description.readAsList()
        self.slateInfo.feedback = self.painter.feedback.readAsList()
        
            #'/JGHome/xiangquan/oiio_test'
        inputFile = self.transferInfo.input.textUnicode()
        fileName = self.inOutput[1]
        fileFolder = fileName.split('.')[0]
        outputPath ="D:/TronDailies/%s/%s" %(fileFolder,fileName)
        outputFolder = "D:/TronDailies/%s" %fileFolder
        #print outputFolder
        if not os.path.isdir(outputFolder):
            os.makedirs(outputFolder)
        #print outputPath
        if not self.checkFileLegal(inputFile):
            self.statusbar.showMessage(Config.winError)
            QMessageBox .critical(self, 'ERROR', u' 不存在的序列: %s ' % inputFile, QString('OK'))
            return

        fstImg = int(self.slateInfo.duration.split(' - ')[0])
        if fstImg == 0:
            self.statusbar.showMessage(Config.winError)
            QMessageBox .critical(self, 'ERROR', u' ERROR：序列起始帧为0', QString('OK'))
            return
            
        if Config.doubleInput:
            inputFile2 = self.transferInfo.input2.textUnicode()
            if not self.checkFileLegal(inputFile2):
                self.statusbar.showMessage(Config.winError)
                QMessageBox .critical(self, 'ERROR', u' 不存在的序列: %s ' % inputFile2, QString('OK'))
                return
        
        hasOutputName = False
        if not os.path.isdir(outputPath):
            print os.path.splitext(outputPath)
            if os.path.splitext(outputPath)[-1] != '.mov':
                self.statusbar.showMessage(Config.winError)
                QMessageBox .critical(self, 'ERROR', u' 不存在的输出目录: %s ' % outputPath, QString('OK'))
                return
            else:
                hasOutputName = True
                outputname = os.path.basename(outputPath)
                outputPath = os.path.dirname(outputPath)
                
        dpxtc = self.transferInfo.dpxtc.textUnicode()
        if not self.checkFileLegal(dpxtc):
            continued = QMessageBox.question(self, 'QUESTION', u'无效的dpx序列，是否继续？', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if continued == QMessageBox.No:
                self.statusbar.showMessage(Config.winError)
                return
#        
        running = True
        outputSlate = ''
        try:
            #draw watermarked imgs; we have to call drawMask() first, 
            #cause Config.FINALTMPFOLDER which is an important param in the drawSlate() is created in this function
            self.statusbar.showMessage(Config.winRun)
            finalImgSize, movRes, fstShotname, running =  self.drawMask(imgSize, outputPath)

            #draw slate
            if running:

                    outputSlate, running = self.drawSlate(finalImgSize, fstShotname, self.slateInfo)
            else:
                self.statusbar.showMessage(Config.winError)
                
            #convert to photo-jpeg
            if running:
                if not hasOutputName:
                    fstShotname += '.mov'
                    self.ffmpegConvert(outputSlate, fstShotname, outputPath)
                else:
                    self.ffmpegConvert(outputSlate, outputname, outputPath)
            else:
                self.statusbar.showMessage(Config.winError)
                
           #delete tmp folder
            if  os.path.exists(Config.FINALTMPFOLDER):
                self.deleteTmpFolder()
            
        except OSError, e:
            self.statusbar.showMessage(Config.winError)
            QMessageBox .critical(self, 'ERROR', u' Response::run(): %s' % str(e).decode('utf-8') , QString('OK'))
            return
            
        self.statusbar.showMessage(Config.winDone)
        QMessageBox.information(self, 'INFORMATION', u'转换完成！', QString('OK'))
        if os.path.isfile(outputPath + '/' + fileName):
            QMainWindow.close(self)


    def checkFileLegal(self, fullpath):
        """ """
        dir = os.path.dirname(fullpath)
        if not os.path.isdir(dir):
            return False
            
        file = os.path.basename(fullpath)
        prefix = file.split('.')[0]
        files = os.listdir(dir)
        for file in files:
            if prefix in file:
                return True
        
        return False
        
    def drawMask(self, imgSize, outputPath):
        """ """
        running = True
        movRes = QSize(imgSize)
#        print 'origin movRes:', movRes
        if Config.resIndex == Config.HD:        #HD
            finalImgSize = QSize(1920,  1080)
            width, height = FnImgHandle.HDSize(movRes)
            movRes = QSize(width, height)
        else:
            finalImgSize = movRes
#        print 'ImgW and H:', movRes
        
        if self.slateInfo.maskRatio != 'square':
            mr = self.slateInfo.maskRatio.split(' : ')
            maskRatio = float(mr[0]) / float(mr[1])
        else:
            maskRatio = 1.0
#        print "maskRatio:", maskRatio

        mskOpc = self.transferInfo.maskOpc.textStr()
        opacity = Config.halfOpc
        if mskOpc == 'Half Mask':
            opacity = Config.halfOpc
        elif mskOpc == 'Full Mask':
            opacity = Config.fullOpc
        elif mskOpc == 'No Mask':
            opacity = Config.noOpc
            
        #get dpx timecode
        dpx = self.transferInfo.dpxtc.textStr()
        dpxDirAnalyse = DirAnalyse(dpx)
        dpxname = dpxDirAnalyse.shotname
        dpxPath = dpxDirAnalyse.path
        
        #draw watermarked imgs
        fstShotname = self.painter.dirAnalyse.shotname
        fstPath = self.painter.dirAnalyse.path
        #print 'response::fstPath:', fstPath
        if self.painter.dirAnalyse.fullpath.split('.')[-1] in Config.TOJPG:
            fstPath = FnImgHandle.convertImgsToJpgs(self.painter.dirAnalyse.files, fstPath, outputPath)
            Config.SPECIMGFOLDER0 = fstPath
            #print 'response::fstPath:', fstPath
         
        if Config.doubleInput:
            secDirAnalyse = DirAnalyse(self.transferInfo.input2.textUnicode())
            secShotname = secDirAnalyse.shotname
            secPath = secDirAnalyse.path
            #print 'response::secPath:', secPath
            if secDirAnalyse.fullpath.split('.')[-1] in Config.TOJPG:
                secPath = FnImgHandle.convertImgsToJpgs(secDirAnalyse.files, secPath, outputPath)
                Config.SPECIMGFOLDER = secPath
            #print 'response::secPath:', secPath
            running = FnDrawMask.saveSequence(self.mainWindow, opacity, maskRatio, finalImgSize, movRes, self.slateInfo, outputPath, fstShotname, fstPath, secShotname, secPath ,dpxname, dpxPath)
        else:
            running = FnDrawMask.saveSequence(self.mainWindow, opacity, maskRatio, finalImgSize, movRes, self.slateInfo, outputPath, fstShotname, fstPath, dpxname = dpxname, dpxPath = dpxPath)
            
        return finalImgSize, movRes, fstShotname, running
        
    def drawSlate(self, slateSize, fstShotname, slateInfo):
        """ Collect input path pattern and draw a slate or not """
        """ return running status and path pattern"""
        running = True
        descList = []
        feedbackList = []
        descTextEdit = self.painter.description
        fbTextEdit = self.painter.feedback
        fbTextEdit = self.painter.feedback
        descList = descTextEdit.readAsList()
        feedbackList = fbTextEdit.readAsList()
        
        fstImg = int(self.slateInfo.duration.split(' - ')[0])
        if fstImg != 0:
            slateframe = fstImg - 1
        slateStrFrame = '%04d' % slateframe
        slatename = fstShotname + '.' + slateStrFrame + '.jpg'
#        outputSlate = os.path.join(outputPath, Config.TMPFOLDER)
        outputSlate = Config.FINALTMPFOLDER
        outputSlate = os.path.join(outputSlate, slatename)
        tbImgPath = os.path.join(self.painter.dirAnalyse.path, self.painter.dirAnalyse.files[0])
        #fnDrawSlate = FnDrawSlate(self.painter.title, self.painter.ver)
        running = True
        return outputSlate, running
        
    def ffmpegConvert(self, outputSlate, fstShotname, outputPath):
        """ organize ffmpeg cmd and convert seq to mov"""
        fps = self.transferInfo.fpsCombo.textStr()
        nameSplit = outputSlate.split('.')
        startframe = nameSplit[1]
        vcodec = self.transferInfo.vcodec.textStr()
        if vcodec == 'mjpeg':
            fvcodec  = 'mjpeg'
        elif vcodec =='h264':
            fvcodec =  'libx264 -profile:v baseline -preset veryslow -crf 20'
        elif vcodec == 'lossless':
            fvcodec = 'copy'

        if platform.system() == 'Linux' or platform.system() == 'Darwin':
            input = nameSplit[0] + '.%04d.' + nameSplit[-1] 
            output = os.path.join(outputPath, fstShotname)
#            cmd = '/Public/Ptd/Softwares/ffmpeg_ubuntu_20130522/bin/ffmpeg -y -probesize 500000000 -f image2 -r %s -start_number %s -i %s \
#                 -an -vcodec %s -s %s -qmin 0.1 -qmax 1 -b:v 1000k -bt 1000M -f mov %s' % (fps, startframe, input, fvcodec, self.slateInfo.resolution, output)
            if vcodec == 'h264':
                cmd = 'ffmpeg -y -f image2 -r %s -start_number %s -i %s \
                 -an -vcodec %s -s %s -f mov %s' % (fps, startframe, input, fvcodec, self.slateInfo.resolution, output)
#            elif vcodec == 'mjpeg':
#                cmd = 'ffmpeg -y -probesize 50000 -f image2 -r %s -start_number %s -i %s \
#                 -an -vcodec %s -s %s -q 15 -b:v 50k -bt 5M -f mov %s' % (fps, startframe, input, fvcodec, self.slateInfo.resolution, output)
            else:
                cmd = 'ffmpeg -y -probesize 500000000 -f image2 -r %s -start_number %s -i %s \
                 -an -vcodec %s -s %s -qmin 0.1 -qmax 1 -b:v 1000k -bt 1000M -f mov %s' % (fps, startframe, input, fvcodec, self.slateInfo.resolution, output)
            try:
                os.popen(cmd)
            except Exception as e:
                QMessageBox .critical(self, 'ERROR', u' Response::ffmpegConvert(): %s ' % str(e).decode('utf-8'), QString('OK'))
                
        elif platform.system() == 'Windows':
            input = nameSplit[0] + '.%04d.' + nameSplit[-1] 
            input = input.replace('\\', '/')
            output = os.path.join(outputPath, fstShotname)
            print platform.system()
            if vcodec == 'h264':
                cmd = 'W:/tronPipelineScript/IlluminaConverter_v002/ffmpeg_win_20130514/bin/ffmpeg -y -f image2 -r %s -start_number %s -i %s \
                 -an -vcodec %s -s %s -f mov %s' % (fps, startframe, input, fvcodec, self.slateInfo.resolution, output)
            else:
                cmd = 'W:/tronPipelineScript/IlluminaConverter_v002/ffmpeg_win_20130514/bin/ffmpeg -y -probesize 500000000 -f image2 -r %s -start_number %s -i %s \
                -an -vcodec %s -s %s -qmin 0.1 -qmax 1 -b:v 1000k -bt 1000M -f mov %s' % (fps, startframe, input, fvcodec, self.slateInfo.resolution, output)
            try:
                os.system(cmd)
            except Exception as e:
                QMessageBox .critical(self, 'ERROR', u' Response::ffmpegConvert(): %s ' % str(e).decode('utf-8'), QString('OK'))

            
        #print 'cmd:', cmd    
        
    def deleteTmpFolder(self):
        """ """
        if os.path.exists(Config.FINALTMPFOLDER):
#            print 'finaltmpfolder:', Config.FINALTMPFOLDER
            shutil.rmtree(Config.FINALTMPFOLDER)
            
        if os.path.exists(Config.SPECIMGFOLDER0):
#            print 'specimgfolder0:', Config.SPECIMGFOLDER0
            shutil.rmtree(Config.SPECIMGFOLDER0)
            
        if os.path.exists(Config.SPECIMGFOLDER):
#            print 'specimgfolder:', Config.SPECIMGFOLDER
            shutil.rmtree(Config.SPECIMGFOLDER)
            
        if platform.system() == 'Linux':
            tb = os.path.join(os.environ['HOME'], '.thumbnail.jpg')
            if os.path.exists(tb):
                os.remove(tb)
            tb2 = os.path.join(os.environ['HOME'], '.thumbnail2.jpg')
            if os.path.exists(tb2):
                os.remove(tb2)
                
        elif platform.system() == 'Windows':
            if os.path.exists('D:/.thumbnail.jpg'):
#                print 'thumbnail.jpg exists'
                os.remove('D:/.thumbnail.jpg')

            if os.path.exists('D:/.thumbnail2.'
                              'jpg'):
#                print 'thumbnail2.jpg exists'
                os.remove('D:/.thumbnail2.jpg')
            
        Config.FINALTMPFOLDER = ''
        Config.SPECIMGFOLDER0 = ''
        Config.SPECIMGFOLDER = ''

