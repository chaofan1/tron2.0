#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
# Filename: saveFileWindows.py

import os,shutil,platform
import createThumbnail
import httpUrl
import cv2
from PyQt4.QtGui import *
from PyQt4.QtCore import *


def SelectReferenceWin(serverName,filePath,fileName,fileID,UpTask):
    import sys
    if platform.system() == 'Darwin':
        inPathFile = '/Users'
    else:
        inPathFile = "D:/"

    app = QApplication(sys.argv)
    app.setStyle('windows')
    app.setStyleSheet('QMainWindow {border:0px solid black;background:rgb(255, 255, 255)}')
    mainWindow = QMainWindow()
    mainWindow.setWindowFlags(Qt.WindowStaysOnTopHint)
    fileOld = QFileDialog.getOpenFileName(mainWindow, QString(), inPathFile,
                                          '*.* \n*.mov \n*.mp4 \n*.avi \n*.jpg *.jpeg \n%.png \n*.tiff \n*.tga *.dpx \n*.*',
                                          options=QFileDialog.ReadOnly)
    if fileOld:
        fileType = fileOld.split(".")[-1]
        if os.path.isfile(fileOld):
            shutil.copy(fileOld, (serverName+filePath + "/" + fileName + "." + fileType))
            print (serverName+filePath + "/" + fileName + "." + fileType)
            fileNow = (fileName + "." + fileType)
            if os.path.exists((serverName+filePath + "/" + fileName + "." + fileType)):
                if fileType == "mov" or fileType =="avi" or fileType =="mp4":
                    createThumbnail.run(fileNow, (serverName+filePath))
                    httpUrl.toHttpask(fileID, filePath, fileNow, UpTask,"")
                elif fileType == "jpg" or fileType == "jpeg" or fileType == "png" or fileType == "tiff" or fileType == "tga":
                    img = cv2.imread(serverName + filePath + "/" + fileName + "." + fileType)
                    pic_high, pic_width, numsd = img.shape
                    thumbWidth = 203
                    thumbHigh = int(pic_high / (pic_width / thumbWidth))
                    img_out = cv2.resize(img, (thumbWidth, thumbHigh), interpolation=cv2.INTER_CUBIC)
                    cv2.imwrite((serverName + filePath + "/." + fileName + "." + fileType), img_out)
                    httpUrl.toHttpask(fileID, filePath, fileNow, UpTask, "")
                QMessageBox.information(None, 'INFORMATION', u"提交成功！", QString('OK'))
                return (filePath + "/" + fileName)
            else:
                QMessageBox.information(None, 'INFORMATION', u"提交失败，请检查上传文件", QString('OK'))
                return filePath
    else:
        return filePath
    sys.exit(app.exec_())

