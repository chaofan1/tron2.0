#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
# Filename: saveFileWindows.py

import os,shutil,platform
import createThumbnail
import httpUrl
import cv2
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys


def SelectDailiesWin(serverName,filePath,fileName,command_id,UpTask):
    inPathFile = '/Users'

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
        fileNow = (fileName + "." + fileType)

        # 重构filePath: /FUY/stuff/dmt
        if fileType == "mov" or fileType == "avi" or fileType == "mp4":
            filePath = filePath + '/mov'
        elif fileType == "jpg" or fileType == "jpeg" or fileType == "png" or fileType == "tiff" or fileType == "tga":
            filePath = filePath + '/img'

        if platform.system() == 'Darwin':
            outPAt = os.environ['HOME']
            outputPath = "%s/%s/%s" % (outPAt, fileName, fileNow)
            outputFolder = "%s/%s" % (outPAt, fileName)
        if os.path.isdir(outputFolder):
            shutil.rmtree(outputFolder)
        os.makedirs(outputFolder)
        shutil.copy(fileOld, outputPath)
        if os.path.exists((serverName + filePath + "/" + fileName + "/")):
            shutil.rmtree((serverName + filePath + "/" + fileName + "/"))
        shutil.copytree(outputFolder, (serverName + filePath + "/" + fileName + "/"))
        if os.path.isfile(outputPath):
            print outputFolder
            if os.path.exists((serverName + filePath + "/" + fileName + "/")):
                shutil.rmtree((serverName + filePath + "/" + fileName + "/"))
            shutil.copytree(outputFolder, (serverName + filePath + "/" + fileName + "/"))
            file_abspath = serverName + filePath + "/" + fileName + "/" + fileNow
            if os.path.exists(file_abspath):
                if fileType == "mov" or fileType == "avi" or fileType == "mp4":
                    createThumbnail.run(fileNow, (serverName + filePath + "/" + fileName))
                    httpUrl.toHttpask(command_id, (filePath + "/" + fileName), fileNow, UpTask, "")
                    QMessageBox.information(None, 'INFORMATION', u"提交成功！", QString('OK'))
                elif fileType == "jpg" or fileType == "jpeg" or fileType == "png" or fileType == "tiff" or fileType == "tga":
                    img = cv2.imread(file_abspath)
                    cv2.imwrite(file_abspath, img, [int(cv2.IMWRITE_JPEG_QUALITY), 40])
                    httpUrl.toHttpask(command_id, filePath + "/" + fileName, fileNow, UpTask, "")
                    QMessageBox.information(None, 'INFORMATION', u"提交成功！", QString('OK'))
                return filePath + "/" + fileName
            else:
                QMessageBox.information(None, 'INFORMATION', u"提交失败，请检查上传文件", QString('OK'))
                return filePath
    else:
        return filePath

    sys.exit(app.exec_())

